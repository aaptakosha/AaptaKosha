#!/usr/bin/env python3
"""Conservative historical ṭīkā ingester for explicitly identified commentators.

Current adapter: Ayana's Sushruta pages exposing Dalhaṇa's Nibandhasaṅgraha.
It never treats an educational English explanation as ṭīkā. Only the Sanskrit
commentary block following a śloka and an explicit Dalhaṇa/Nibandhasaṅgraha
identity marker is accepted.
"""
from __future__ import annotations
import argparse, hashlib, json, re, ssl
from datetime import datetime, timezone
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urlparse
from urllib.request import Request, urlopen

ROOT=Path(__file__).resolve().parents[1]
QUEUE=ROOT/"content/.automation/source-verification-queue.json"
OUT=ROOT/"content/samhita/sushruta/sutrasthana"
DEV=re.compile(r"[\u0900-\u097F]")
ADH=re.compile(r"Adhikarana .*?Śloka\s+([०-९0-9]+)")
DAL=re.compile(r"(डल्हण|डल्हणाचार्य|श्रीडल्हण|निबन्धसङ्ग्रह|निबन्धसंग्रह|Dalhaṇa|Dalhana)")
STOP={"Meaning of the commentary","Meaning of the śloka","Key terms","Audio coming soon","🔊 Audio coming soon"}
DIG="०१२३४५६७८९"
def now(): return datetime.now(timezone.utc).isoformat()
def num(s):
    return int(''.join(str(DIG.index(c)) if c in DIG else c for c in s))
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
        raw=r.read(); return raw.decode("utf-8","replace")
def parse(url,raw):
    lines=P(); lines.feed(raw); L=lines.lines
    whole="\n".join(L)
    chapter_number=None
    for line in L[:40]:
        m=re.match(r"(?:#\\s*)?([०-९0-9]{1,3})\\.\\s+", line)
        if m:\n            chapter_number=num(m.group(1)); break
    if not DAL.search(whole): return None
    blocks=[]; current=None; collecting=False; buf=[]
    for line in L:
        m=ADH.search(line)
        if m:
            if current and buf:
                blocks.append((current," ".join(x for x in buf if DEV.search(x))))
            current=num(m.group(1)); buf=[]; collecting=False; continue
        if not current: continue
        if line in STOP: 
            if line=="🔊 Audio coming soon": collecting=True
            continue
        if collecting and DEV.search(line):
            # English/educational prose is rejected by DEV check; source commentary is Sanskrit.
            buf.append(line)
    if current and buf: blocks.append((current," ".join(x for x in buf if DEV.search(x))))
    return {"url":url,"commentator":"Dalhaṇa","chapter_number":chapter_number,"blocks":[{"verse_number":n,"tika_sanskrit":t} for n,t in blocks if len(t)>10]}
def main():
    ap=argparse.ArgumentParser(); ap.add_argument("--limit",type=int,default=100); args=ap.parse_args()
    if not QUEUE.exists(): print(json.dumps({"status":"no_queue"})); return
    q=json.loads(QUEUE.read_text(encoding="utf-8"))
    urls=[]
    for item in q.get("items",[]):
        for s in item.get("sources",[]):
            urls.append(s.get("url"))
            urls += s.get("linked_urls",[])
    urls=list(dict.fromkeys(u for u in urls if u and "ayanaayurveda.com" in (urlparse(u).hostname or "")))[:args.limit]
    staged=[]; seen=0
    for url in urls:
        try: raw=fetch(url)
        except Exception as e:
            staged.append({"url":url,"status":"fetch_failed","error":str(e)}); continue
        p=parse(url,raw)
        if not p: continue
        sha=hashlib.sha256(raw.encode()).hexdigest()
        p["retrieved_at"]=now(); p["content_sha256"]=sha; p["status"]="source_verified_commentary_candidate"
        staged.append(p); seen+=len(p["blocks"])
    target=ROOT/"content/.automation/tika-verification-queue.json"
    target.write_text(json.dumps({"schema_version":1,"generated_at":now(),"policy":"Only explicitly identified historical commentary; no generated tika.","pages":staged,"block_count":seen},ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    print(json.dumps({"pages_scanned":len(urls),"commentary_blocks":seen,"queue":str(target.relative_to(ROOT))},ensure_ascii=False,indent=2))
if __name__=="__main__": main()
