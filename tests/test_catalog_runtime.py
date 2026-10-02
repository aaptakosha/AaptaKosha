from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def test_catalog_uses_a_single_sqlite_fallback_path():
    source = (ROOT / "api" / "catalog.py").read_text(encoding="utf-8")
    assert "def _sqlite_repo():" in source
    assert "postgres curriculum snapshot missing" in source
    assert "CONNECTION, REPO = _sqlite_repo()" in source
    assert source.count("CATALOG_MIGRATIONS = (") == 1
    assert source.count("for migration in CATALOG_MIGRATIONS") == 1


def test_catalog_fallback_manifest_matches_repository_migrations():
    source = (ROOT / "api" / "catalog.py").read_text(encoding="utf-8")
    import re
    migrations = re.findall(r'"([0-9]+_[^"]+\\.sql)"', source)
    migration_dir = ROOT / "migrations"
    missing = [name for name in migrations if not (migration_dir / name).exists()]
    assert missing == []
