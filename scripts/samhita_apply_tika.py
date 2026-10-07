#!/usr/bin/env python3
"""Promote source-verified historical ṭīkā blocks into existing chapter records.

Only blocks with an explicit commentator identity and chapter/śloka anchor are
attached. Existing tika arrays are preserved and deduplicated.
"""
from __future__ import annotations
import argparse, hashlib, json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
QUEUE=ROOT/"content/.automation/tika-verification-queue.json"
OUT=ROOT/"content/samhita/sushruta/sutrasthana"
AUTOPILOT_VERSION="2026-10-07-source-ingestion-v1"\n\ndef main():
    ap=argparse.ArgumentParser(); ap.add_argument("--limit",type=int,default=1000); args=ap.parse_args()
    if not QUEUE.exists(): print(json.dumps({"status":"no_queue"})); return
    q=json.loads(QUEUE.read_text(encoding="utf-8"))
    attached=0; pages=0; skipped=0
    for page in q.get("pages",[])[:args.limit]:
        if page.get("status")!="source_verified_commentary_candidate" or page.get("commentator")!="Dalhaṇa": continue
        ch=page.get("chapter_number")
        if not ch: skipped+=1; continue
        path=OUT/f"adhyaya-{int(ch):02d}.json"
        if not path.exists(): skipped+=1; continue
        obj=json.loads(path.read_text(encoding="utf-8"))
        passages=obj.get("passages") or obj.get("verses") or []
        changed=False
        for block in page.get("blocks",[]):
            vn=block.get("verse_number")
            if vn is None: continue
            for p in passages:
                if str(p.get("verse_number")) != str(vn): continue
                tika=p.setdefault("tika",[])
                if not isinstance(tika,list): tika=[]
                digest=hashlib.sha256(block["tika_sanskrit"].encode("utf-8")).hexdigest()
                if any(isinstance(t,dict) and t.get("content_sha256")==digest for t in tika):
                    break
                tika.append({
                    "commentator":"Dalhaṇa",
                    "title":"Nibandhasaṅgraha",
                    "sanskrit_original":block["tika_sanskrit"],
                    "source_url":page["url"],
                    "source_retrieved_at":page.get("retrieved_at"),
                    "content_sha256":digest,
                    "source_status":"source_verified"
                })
                attached+=1; changed=True; break
        if changed:
            obj.setdefault("verification",{})["tika_status"]="source_verified"
            path.write_text(json.dumps(obj,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
            pages+=1
    print(json.dumps({"pages_updated":pages,"tika_blocks_attached":attached,"skipped":skipped},ensure_ascii=False,indent=2))
if __name__=="__main__": main()
