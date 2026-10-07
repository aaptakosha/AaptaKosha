#!/usr/bin/env python3
"""Conservative historical tika ingester for explicitly identified commentators."""
from __future__ import annotations
import argparse, hashlib, json, re, ssl
from datetime import datetime, timezone
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urlparse
from urllib.request import Request, urlopen

ROOT=Path(__file__).resolve().parents[1]
QUEUE=ROOT/"content/.automation/source-verification-queue.json"
DEV=re.compile(r"[\u0900-\u097F]")
ANCHOR=re.compile(r"Adhikarana\s+([०-९0-9]+)(?:\s*\([^)]*\))?\s*[·•]\s*Śloka\s+([०-९0-9]+)", re.I)
DAL=re.compile(r"(डल्हण|डल्हणाचार्य|श्रीडल्हण|निबन्धसङ्ग्रह|निबन्धसंग्रह|Dalhaṇa|Dalhana)")
DIG="०१२३४५६७८९"

def now(): return datetime.now(timezone.utc).isoformat()
def num(s): return int("".join(str(DIG.index(c)) if c in DIG else c for c in s))

class P(HTMLParser):
    def __init__(self): super().__init__(); self.lines=[]; self.skip=0
    def handle_starttag(self,t,a):
        if t in {"script","style","noscript","svg"}: self.skip+=1
    def handle_endtag(self,t):
        if t in {"script","style","noscript","svg"} and self.skip: self.skip-=1
    def handle_data(self,d):
        if not self.skip and d.strip(): self.lines.append(re.sub(r"\s+"," ",d).strip())

def fetch(url):
    req=Request(url,headers={"User-Agent":"AaptaKosha-Samhita-Autopilot/1.0"})
    with urlopen(req,timeout=60,context=ssl.create_default_context()) as r:
        return r.read().decode("utf-8","replace")

def plain_text(raw):
    import html
    text=re.sub(r"<(script|style|noscript|svg)\\b[^>]*>.*?</\\1>","\\n",raw,flags=re.I|re.S)
    text=re.sub(r"<[^>]+>"," ",text)
    text=html.unescape(text)
    return re.sub(r"\\s+"," "," ".join(text.splitlines())).strip()

def parse(url,raw):
    text=plain_text(raw)
    if not DAL.search(text): return None
    chapter_number=1 if "vedotpattyadhyayah" in url else None
    blocks=[]
    matches=list(ANCHOR.finditer(text))
    for i,m in enumerate(matches):
        current=num(m.group(2))
        segment=text[m.end(): matches[i+1].start() if i+1<len(matches) else len(text)]
        # Ayana renders the authentic commentary between the commentary toggle
        # and its English explanatory section. Never ingest the English meaning.
        toggle=re.search(r"\\b(?:Hide commentary|Show commentary)\\b",segment)
        if not toggle: continue
        body=segment[toggle.end():]
        stop=re.search(r"\\bMeaning of the commentary\\b|\\bKey terms\\b",body)
        if stop: body=body[:stop.start()]
        # Remove UI/audio labels and keep only Devanagari source text.
        parts=[x.strip() for x in re.split(r"\\s+",body) if DEV.search(x)]
        tika=" ".join(parts)
        if len(tika)>10:
            blocks.append({"verse_number":current,"tika_sanskrit":tika})
    return {"url":url,"commentator":"Dalhaṇa","chapter_number":chapter_number,"blocks":blocks}

def main():
    ap=argparse.ArgumentParser(); ap.add_argument("--limit",type=int,default=100); args=ap.parse_args()
    if not QUEUE.exists(): print(json.dumps({"status":"no_queue"})); return
    q=json.loads(QUEUE.read_text(encoding="utf-8")); urls=[]
    for item in q.get("items",[]):
        for s in item.get("sources",[]):
            if s.get("url"): urls.append(s["url"])
            urls.extend(s.get("linked_urls",[]))
    urls=list(dict.fromkeys(u for u in urls if u and "ayanaayurveda.com" in (urlparse(u).hostname or "") and ("commentary=show" in u or "vedotpattyadhyayah" in u)))[:args.limit]
    staged=[]; seen=0
    for url in urls:
        try: raw=fetch(url)
        except Exception as e: staged.append({"url":url,"status":"fetch_failed","error":str(e)}); continue
        parsed=parse(url,raw)
        if not parsed or not parsed["blocks"]: continue
        parsed["retrieved_at"]=now(); parsed["content_sha256"]=hashlib.sha256(raw.encode("utf-8")).hexdigest(); parsed["status"]="source_verified_commentary_candidate"
        staged.append(parsed); seen+=len(parsed["blocks"])
    target=ROOT/"content/.automation/tika-verification-queue.json"
    target.write_text(json.dumps({"schema_version":1,"generated_at":now(),"policy":"Only explicitly identified historical commentary; no generated tika.","pages":staged,"block_count":seen},ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    print(json.dumps({"pages_scanned":len(urls),"commentary_blocks":seen,"queue":str(target.relative_to(ROOT))},ensure_ascii=False,indent=2))
if __name__=="__main__": main()
