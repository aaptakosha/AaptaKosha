import sqlite3
from aaptakosha_ingestion.pipeline import Artifact,fingerprint_artifact,normalize_curriculum,validate_curriculum,diff_curriculum,reconcile

def curriculum(name="A",topic="T1"):
    return {"curriculum_id":"BAMS","version":"1.0","professional_year":2,
            "subjects":[{"subject_id":"S1","name":name,"topics":[{"topic_id":topic,"name":"Topic"}]}]}

def artifact(data=b"x"):
    return Artifact("SRC-NCISM-II","fixture://curriculum","2026-09-30T00:00:00Z","application/json",data,
        fingerprint_artifact(data,source_id="SRC-NCISM-II",locator="fixture://curriculum"))

def test_normalization_is_deterministic():
    a=normalize_curriculum(curriculum())
    b=normalize_curriculum({"subjects":curriculum()["subjects"],"professional_year":2,"version":"1.0","curriculum_id":"BAMS"})
    assert a==b

def test_validation_rejects_duplicate_ids():
    c=curriculum(); c["subjects"].append(c["subjects"][0].copy())
    assert any(x.startswith("duplicate:subject_id") for x in validate_curriculum(c))

def test_diff_classifies_modify():
    events=diff_curriculum(curriculum(),curriculum(name="Changed",topic="T2"))
    assert "MODIFY" in {e["classification"] for e in events}

def test_reconcile_publishes_and_records_changes(tmp_path):
    db=tmp_path/"a.db"; result=reconcile(db,"SRC-NCISM-II",artifact(),curriculum())
    assert result["status"]=="PUBLISHED"
    con=sqlite3.connect(db)
    assert con.execute("select count(*) from artifacts").fetchone()[0]==1
    assert con.execute("select count(*) from curriculum_versions").fetchone()[0]==1
    con.close()

def test_review_blocks_publication(tmp_path):
    db=tmp_path/"b.db"; result=reconcile(db,"SRC-NCISM-II",artifact(b"y"),curriculum(),require_review=True)
    assert result["status"]=="REVIEW"
    con=sqlite3.connect(db)
    assert con.execute("select count(*) from curriculum_versions").fetchone()[0]==0
    assert con.execute("select count(*) from review_queue").fetchone()[0]==1
    con.close()
