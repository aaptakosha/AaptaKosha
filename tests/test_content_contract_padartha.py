from pathlib import Path
import re
from aaptakosha_core.content_contract import validate_markdown, CONTENT_STANDARD_VERSION

ROOT = Path(__file__).resolve().parents[1]
PADARTHA = ROOT / "content" / "padartha-vijnanam"

def test_universal_standard_version():
    assert CONTENT_STANDARD_VERSION == "2.0"

def test_all_padartha_chapters_pass_universal_contract():
    files = sorted(PADARTHA.glob("*.md"))
    assert len(files) == 16
    for path in files:
        result = validate_markdown(path.read_text(encoding="utf-8"))
        assert result.valid, (path.name, result.errors)

def test_padartha_curriculum_api_maps_all_16_nodes():
    source = (ROOT / "api" / "content.py").read_text(encoding="utf-8")
    for i in range(1, 17):
        assert f'"y1-pv-{i}"' in source
    assert 'CONTENT_STANDARD_VERSION' in source
    assert 'content_schema_validation_failed' in source
