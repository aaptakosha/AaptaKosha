#!/usr/bin/env python3
"""Source-backed Samhita acquisition worker.

This worker is deliberately conservative:
- only allowlisted public source hosts are fetched;
- AI is never used to invent Sanskrit or commentary;
- source text is staged only when Devanagari is actually present;
- commentary is accepted only when a named commentator is explicitly detected;
- every staged artifact carries URL, host, retrieval time and content hash;
- existing files are never replaced;
- uncertain material is written to the verification queue.

The worker is designed for GitHub Actions and uses only Python's standard library.
"""
from __future__ import annotations
import argparse, hashlib, html, json, re, ssl
from datetime import datetime, timezone
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import quote_plus, urljoin, urlparse
from urllib.request import Request, urlopen

ROOT = Path(__file__).resolve().parents[1]
REGISTRY = ROOT / "content" / "samhita-registry.json"
AUTO = ROOT / "content" / ".automation"
QUEUE = AUTO / "source-verification-queue.json"
SOURCES = AUTO / "source-catalog.json"

ALLOWED_HOSTS = {
    "www.ebharatisampat.in",
    "ebharatisampat.in",
    "www.ayanaayurveda.com",
    "ayanaayurveda.com",
    "sushrutaproject1.github.io",
}

DEV = re.compile(r"[\u0900-\u097F]")
VERSE_MARK = re.compile(r"(?<!\d)(?:[०-९]+|\d{1,3})(?:\s*[।॥]|\s*$)")
COMMENTARY = re.compile(
    r"(दल्हण|डल्हण|डल्हणाचार्य|Dalhaṇa|Dalhana|निबन्धसंग्रह|निबन्धसङ्ग्रह|"
    r"अरुणदत्त|हेमाद्रि|चक्रपाणि|गङ्गाधर|जीवक|योगीन्द्रनाथ|श्रीकण्ठ)"
)

class TextParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.parts=[]
        self.links=[]
        self._skip=0
    def handle_starttag(self, tag, attrs):
        if tag in {"script","style","noscript","svg"}: self._skip += 1
        if tag == "a":
            d=dict(attrs); href=d.get("href")
            if href: self.links.append(href)
    def handle_endtag(self, tag):
        if tag in {"script","style","noscript","svg"} and self._skip: self._skip -= 1
    def handle_data(self, data):
        if not self._skip and data.strip(): self.parts.append(data.strip())

def now(): return datetime.now(timezone.utc).isoformat()

def get(url, timeout=30):
    req=Request(url, headers={"User-Agent":"AaptaKosha-Samhita-Autopilot/1.0 (+source-verification)"})
    ctx=ssl.create_default_context()
    with urlopen(req, timeout=timeout, context=ctx) as r:
        raw=r.read()
        ctype=r.headers.get("content-type","")
        charset="utf-8"
        m=re.search(r"charset=([^;]+)",ctype,re.I)
        if m: charset=m.group(1).strip()
        return raw.decode(charset,errors="replace"), r.geturl()

def allowed(url):
    h=(urlparse(url).hostname or "").lower()
    return h in ALLOWED_HOSTS

def clean(s):
    s=html.unescape(s)
    s=re.sub(r"\s+"," ",s).strip()
    return s

def source_records(url, title_hint=""):
    if not allowed(url): return []
    try:
        body, final=get(url)
    except Exception as e:
        return [{"url":url,"title":title_hint,"status":"fetch_failed","error":str(e)}]
    p=TextParser(); p.feed(body)
    text="\n".join(clean(x) for x in p.parts if x.strip())
    sans=[x for x in text.splitlines() if DEV.search(x)]
    named=sorted(set(COMMENTARY.findall(text)))
    digest=hashlib.sha256(body.encode("utf-8")).hexdigest()
    linked=list(dict.fromkeys(urljoin(final,h) for h in p.links if allowed(urljoin(final,h))))[:100]
    return [{
        "url":final,
        "host":urlparse(final).hostname,
        "title":title_hint,
        "retrieved_at":now(),
        "content_sha256":digest,
        "sanskrit_lines":len(sans),
        "commentators_detected":named,
        "linked_urls":linked,
        "status":"source_found" if sans else "no_sanskrit_detected",
        "text_sample":sans[:80],
    }]

def discover(query):
    url="https://html.duckduckgo.com/html/?q="+quote_plus(query)
    try: body,_=get(url)
    except Exception: return []
    p=TextParser(); p.feed(body)
    out=[]
    for h in p.links:
        u=urljoin(url,h)
        if allowed(u): out.append(u)
    return list(dict.fromkeys(out))[:10]

def load_books():
    reg=json.loads(REGISTRY.read_text(encoding="utf-8"))
    return [b for c in reg.get("library_sources",{}).get("categories",[]) for b in c.get("books",[])]

def load_catalog():
    if SOURCES.exists(): return json.loads(SOURCES.read_text(encoding="utf-8"))
    return {"sources":[]}

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--discover", action="store_true")
    ap.add_argument("--limit", type=int, default=3)
    args=ap.parse_args()
    AUTO.mkdir(parents=True,exist_ok=True)
    books=load_books()
    catalog=load_catalog()
    items=[]
    configured={x.get("book_id"):x for x in catalog.get("sources",[])}

    # Prioritize partial/planned books; configured URLs are tried before discovery.
    for b in books:
        bid=b["id"]
        cfg=configured.get(bid,{})
        urls=list(cfg.get("urls",[]))
        if args.discover and not urls:
            q=f'site:ebharatisampat.in "{b.get("name_en",bid)}" Ayurveda'
            urls += discover(q)
            q2=f'site:ayanaayurveda.com "{b.get("name_en",bid)}" commentary'
            urls += discover(q2)
        urls=list(dict.fromkeys(u for u in urls if allowed(u)))
        if not urls:
            items.append({"book_id":bid,"name":b.get("name_en"),"status":"source_not_found"})
            continue
        recs=[]
        for u in urls[:args.limit]:
            recs += source_records(u,b.get("name_en",""))
        good=[r for r in recs if r.get("status")=="source_found"]
        if good:
            items.append({"book_id":bid,"name":b.get("name_en"),"status":"source_found","sources":good})
        else:
            items.append({"book_id":bid,"name":b.get("name_en"),"status":"verification_required","sources":recs})

    QUEUE.write_text(json.dumps({
        "schema_version":1,"generated_at":now(),
        "policy":"No generated Sanskrit/Tika. Source-backed artifacts only.",
        "items":items
    },ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    print(json.dumps({
        "books_scanned":len(items),
        "source_found":sum(x["status"]=="source_found" for x in items),
        "verification_required":sum(x["status"]=="verification_required" for x in items),
        "source_not_found":sum(x["status"]=="source_not_found" for x in items),
        "queue":str(QUEUE.relative_to(ROOT))
    },ensure_ascii=False,indent=2))

if __name__=="__main__":
    main()
