"""Dependency-free Phase 1 ingestion/reconciliation engine."""
from __future__ import annotations
import hashlib, json, sqlite3, time
from dataclasses import dataclass
from pathlib import Path
from typing import Any
from urllib.request import Request, urlopen

SCHEMA_VERSION="1.0"

@dataclass(frozen=True)
class Artifact:
    source_id:str
    locator:str
    retrieved_at:str
    media_type:str
    content:bytes
    fingerprint:str

def fingerprint_artifact(content:bytes, *, source_id:str, locator:str)->str:
    payload=source_id.encode()+b"\0"+locator.encode()+b"\0"+content
    return hashlib.sha256(payload).hexdigest()

def capture_artifact(source_id:str, locator:str, *, timeout:int=30, max_attempts:int=3, backoff_seconds:float=0.2)->Artifact:
    last_error=None
    for attempt in range(1,max_attempts+1):
        try:
            if locator.startswith(("http://","https://")):
                req=Request(locator,headers={"User-Agent":"AaptaKosha/1.0"})
                with urlopen(req,timeout=timeout) as response:
                    content=response.read()
                    media_type=response.headers.get_content_type() or "application/octet-stream"
            else:
                content=Path(locator).read_bytes()
                media_type="application/octet-stream"
            retrieved_at=time.strftime("%Y-%m-%dT%H:%M:%SZ",time.gmtime())
            return Artifact(source_id,locator,retrieved_at,media_type,content,
                            fingerprint_artifact(content,source_id=source_id,locator=locator))
        except Exception as exc:
            last_error=exc
            if attempt < max_attempts:
                time.sleep(backoff_seconds*(2**(attempt-1)))
    raise RuntimeError(f"artifact capture failed after {max_attempts} attempts: {last_error}")
def normalize_curriculum(raw:dict[str,Any])->dict[str,Any]:
    required=("curriculum_id","version","professional_year","subjects")
    missing=[k for k in required if k not in raw]
    if missing: raise ValueError("missing required fields: "+", ".join(missing))
    def clean(v:Any)->Any:
        if isinstance(v,dict): return {k:clean(v[k]) for k in sorted(v)}
        if isinstance(v,list):
            return sorted((clean(x) for x in v),key=lambda x:json.dumps(x,sort_keys=True,ensure_ascii=False))
        return v
    result=clean(raw); result["schema_version"]=SCHEMA_VERSION
    return result

def validate_curriculum(curriculum:dict[str,Any])->list[str]:
    errors=[]
    for field in ("curriculum_id","version","professional_year","subjects"):
        if field not in curriculum: errors.append("missing:"+field)
    if not isinstance(curriculum.get("subjects"),list):
        errors.append("subjects:not-list"); return errors
    ids=set()
    for i,subject in enumerate(curriculum["subjects"]):
        if not isinstance(subject,dict):
            errors.append(f"subjects[{i}]:not-object"); continue
        for field in ("subject_id","name"):
            if not subject.get(field): errors.append(f"subjects[{i}]:missing:{field}")
        sid=subject.get("subject_id")
        if sid and sid in ids: errors.append("duplicate:subject_id:"+sid)
        if sid: ids.add(sid)
    return errors

def _index(curriculum:dict[str,Any])->dict[str,tuple]:
    out={}
    for s in curriculum.get("subjects",[]):
        sid=s.get("subject_id")
        if not sid: continue
        out["subject:"+sid]=("subject",s)
        for t in s.get("topics",[]):
            tid=t.get("topic_id")
            if tid: out["topic:"+tid]=("topic",t)
    return out

def diff_curriculum(previous:dict[str,Any]|None,candidate:dict[str,Any])->list[dict[str,Any]]:
    if previous is None:
        return [{"classification":"ADD","entity_id":k,"after":v[1]} for k,v in sorted(_index(candidate).items())]
    old,new=_index(previous),_index(candidate); events=[]
    for key in sorted(set(old)|set(new)):
        if key not in old: events.append({"classification":"ADD","entity_id":key,"after":new[key][1]})
        elif key not in new: events.append({"classification":"REMOVE","entity_id":key,"before":old[key][1]})
        elif old[key][1]!=new[key][1]:
            events.append({"classification":"MODIFY","entity_id":key,"before":old[key][1],"after":new[key][1]})
    return events

def _connect(db:str|Path)->sqlite3.Connection:
    con=sqlite3.connect(str(db))
    con.executescript("""
    CREATE TABLE IF NOT EXISTS artifacts(
      fingerprint TEXT PRIMARY KEY, source_id TEXT NOT NULL, locator TEXT NOT NULL,
      retrieved_at TEXT NOT NULL, media_type TEXT NOT NULL, content BLOB NOT NULL);
    CREATE TABLE IF NOT EXISTS runs(
      run_id INTEGER PRIMARY KEY AUTOINCREMENT, source_id TEXT NOT NULL,
      fingerprint TEXT, status TEXT NOT NULL, started_at TEXT NOT NULL,
      ended_at TEXT, error TEXT, change_count INTEGER DEFAULT 0);
    CREATE TABLE IF NOT EXISTS curriculum_versions(
      curriculum_id TEXT NOT NULL, version TEXT NOT NULL, payload TEXT NOT NULL,
      fingerprint TEXT NOT NULL, published_at TEXT NOT NULL,
      PRIMARY KEY(curriculum_id,version));
    CREATE TABLE IF NOT EXISTS review_queue(
      id INTEGER PRIMARY KEY AUTOINCREMENT, run_id INTEGER NOT NULL,
      reason TEXT NOT NULL, payload TEXT NOT NULL, status TEXT NOT NULL);
    CREATE TABLE IF NOT EXISTS change_events(
      id INTEGER PRIMARY KEY AUTOINCREMENT, run_id INTEGER NOT NULL,
      classification TEXT NOT NULL, entity_id TEXT NOT NULL, payload TEXT NOT NULL);
    """)
    return con

def publish_version(db:str|Path,curriculum:dict[str,Any],fingerprint:str)->None:
    errors=validate_curriculum(curriculum)
    if errors: raise ValueError("publication blocked: "+"; ".join(errors))
    con=_connect(db)
    try:
        con.execute("BEGIN")
        con.execute("INSERT INTO curriculum_versions(curriculum_id,version,payload,fingerprint,published_at) VALUES(?,?,?,?,datetime('now'))",
                    (curriculum["curriculum_id"],curriculum["version"],json.dumps(curriculum,ensure_ascii=False,sort_keys=True),fingerprint))
        con.commit()
    except Exception:
        con.rollback(); raise
    finally: con.close()

def reconcile(db:str|Path,source_id:str,artifact:Artifact,candidate:dict[str,Any],
              previous:dict[str,Any]|None=None,*,require_review:bool=False)->dict[str,Any]:
    started=time.strftime("%Y-%m-%dT%H:%M:%SZ",time.gmtime()); con=_connect(db); run_id=None
    try:
        cur=con.execute("INSERT INTO runs(source_id,fingerprint,status,started_at) VALUES(?,?,?,?)",
                        (source_id,artifact.fingerprint,"RUNNING",started)); run_id=cur.lastrowid
        con.execute("INSERT OR IGNORE INTO artifacts(fingerprint,source_id,locator,retrieved_at,media_type,content) VALUES(?,?,?,?,?,?)",
                    (artifact.fingerprint,artifact.source_id,artifact.locator,artifact.retrieved_at,artifact.media_type,artifact.content))
        normalized=normalize_curriculum(candidate); errors=validate_curriculum(normalized)
        changes=diff_curriculum(previous,normalized)
        if errors or require_review:
            reason="; ".join(errors) if errors else "manual_review_required"
            con.execute("INSERT INTO review_queue(run_id,reason,payload,status) VALUES(?,?,?,?)",
                        (run_id,reason,json.dumps(normalized,sort_keys=True),"PENDING")); status="REVIEW"
        else:
            con.execute("INSERT INTO curriculum_versions(curriculum_id,version,payload,fingerprint,published_at) VALUES(?,?,?,?,datetime('now'))",
                        (normalized["curriculum_id"],normalized["version"],json.dumps(normalized,ensure_ascii=False,sort_keys=True),artifact.fingerprint)); status="PUBLISHED"
        for event in changes:
            con.execute("INSERT INTO change_events(run_id,classification,entity_id,payload) VALUES(?,?,?,?)",
                        (run_id,event["classification"],event["entity_id"],json.dumps(event,ensure_ascii=False,sort_keys=True)))
        con.execute("UPDATE runs SET status=?,ended_at=?,change_count=? WHERE run_id=?",
                    (status,time.strftime("%Y-%m-%dT%H:%M:%SZ",time.gmtime()),len(changes),run_id))
        con.commit(); return {"run_id":run_id,"status":status,"changes":changes,"errors":errors}
    except Exception as exc:
        con.rollback()
        if run_id is not None:
            con.execute("UPDATE runs SET status='FAILED',ended_at=?,error=? WHERE run_id=?",
                        (time.strftime("%Y-%m-%dT%H:%M:%SZ",time.gmtime()),str(exc),run_id)); con.commit()
        raise
    finally: con.close()


def get_run_status(db:str|Path, run_id:int)->dict[str,Any]:
    con=_connect(db)
    try:
        row=con.execute("SELECT run_id,source_id,fingerprint,status,started_at,ended_at,error,change_count FROM runs WHERE run_id=?",(run_id,)).fetchone()
        if row is None: raise KeyError(f"unknown run_id: {run_id}")
        keys=("run_id","source_id","fingerprint","status","started_at","ended_at","error","change_count")
        return dict(zip(keys,row))
    finally:
        con.close()
