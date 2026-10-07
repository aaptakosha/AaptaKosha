#!/usr/bin/env python3
"""Idempotent, additive Sushruta source ingester.

Primary text source: e-Bharatisampat Sushruta Samhita Unicode text.
It splits the public chapter stream into chapter JSON files without
rewriting any existing chapter. Commentary remains a separate stage.
"""
from __future__ import annotations
import argparse, hashlib, json, re, ssl
from datetime import datetime, timezone
from pathlib import Path
from urllib.request import Request, urlopen

ROOT=Path(__file__).resolve().parents[1]
URL="https://www.ebharatisampat.in/read_chapter.php?bookid=ODEwMTY2NDM1NDE4MTQy"
OUT=ROOT/"content"/"samhita"/"sushruta"/"sutrasthana"
DEV=re.compile(r"[\u0900-\u097F]")
END=re.compile(r"इति\s+सुश्रुतसंहितायां\s+सूत्रस्थाने.*?अध्यायः\s*([०-९]+)")
HEAD=re.compile(r"^(.+अध्यायः)$")
NUM=re.compile(r"(?:\s|^)([०-९]{1,3}|\d{1,3})\s*[।॥]?\s*$")
DIG="०१२३४५६७८९"
def now(): return datetime.now(timezone.utc).isoformat()
def devan(n):
    s=str(n)
    return ''.join(DIG[int(c)] if c.isdigit() else c for c in s)
def fetch():
    req=Request(URL,headers={"User-Agent":"AaptaKosha-Samhita-Autopilot/1.0"})
    with urlopen(req,timeout=60,context=ssl.create_default_context()) as r:
        raw=r.read()
        return raw.decode("utf-8","replace")
def html_text(raw):
    import html
    text = re.sub(r"<(script|style|noscript|svg)\\b[^>]*>.*?</\\1>", "\\n", raw, flags=re.I|re.S)
    text = re.sub(r"<[^>]+>", "\\n", text)
    text = html.unescape(text)
    return [re.sub(r"\\s+", " ", x).strip() for x in text.splitlines() if x.strip()]

def parse_chapters(raw):
    lines=html_text(raw)
    stream="\\n".join(lines)
    matches=list(END.finditer(stream))
    chapters={}
    previous=0
    for m in matches:
        digits=''.join(str(DIG.index(c)) if c in DIG else c for c in m.group(1))
        num=int(digits)
        segment=stream[previous:m.end()]
        if num<=46:
            titles=re.findall(r"[^\\n]{0,120}अध्यायः",segment)
            title=titles[-1].strip() if titles else f"अध्याय {devan(num)}"
            chapters[num]=(title,segment.splitlines(),m.group(0))
        previous=m.end()
    return chapters

def split_passages(lines):
    out=[]; acc=[]
    for line in lines:
        if not DEV.search(line): continue
        acc.append(line)
        m=NUM.search(line)
        if m:
            raw=m.group(1)
            num=int(''.join(str(DIG.index(c)) if c in DIG else c for c in raw))
            out.append((num," ".join(acc)))
            acc=[]
    if acc:
        out.append((None," ".join(acc)))
    # Remove navigation noise accidentally captured.
    return [(n,t) for n,t in out if len(t)>8 and not t.startswith("Chapter ")]
def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--max-chapters",type=int,default=46)
    args=ap.parse_args()
    raw=fetch()
    sha=hashlib.sha256(raw.encode()).hexdigest()
    chapters=parse_chapters(raw)
    OUT.mkdir(parents=True,exist_ok=True)
    created=0; skipped=0
    for n in sorted(chapters):
        if n>args.max_chapters: continue
        path=OUT/f"adhyaya-{n:02d}.json"
        if path.exists():
            skipped+=1; continue
        title,lines,colophon=chapters[n]
        passages=split_passages(lines)
        if not passages: continue
        data={
          "schema_version":1,
          "content_id":f"sushruta.sutra.{n:02d}.autopilot",
          "book_id":"sushruta-samhita",
          "sthana":"sutrasthana",
          "chapter_number":n,
          "chapter_title":title,
          "source_status":"source_verified_pending_cross_source_qa",
          "source_metadata":[{
             "publisher":"E-Bharatisampat",
             "url":URL,
             "retrieved_at":now(),
             "content_sha256":sha,
             "method":"unicode_source_extraction"
          }],
          "verification":{
             "sanskrit_source":"e-Bharatisampat",
             "cross_source_match_required":True,
             "tika_status":"awaiting_separate_commentary_ingest",
             "generated_text_allowed":False
          },
          "passages":[
             {"passage_id":f"sushruta.su.{n:02d}.{i:03d}",
              "verse_number":num,
              "sanskrit_original":text,
              "source_status":"source_verified",
              "tika":[]}
             for i,(num,text) in enumerate(passages,1)
          ],
          "chapter_colophon":colophon
        }
        path.write_text(json.dumps(data,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
        created+=1
    print(json.dumps({"source":URL,"chapters_detected":len(chapters),"created":created,"existing_skipped":skipped,"source_sha256":sha},ensure_ascii=False,indent=2))
if __name__=="__main__": main()
