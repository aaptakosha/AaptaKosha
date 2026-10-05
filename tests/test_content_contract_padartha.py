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
    import importlib.util
    spec = importlib.util.spec_from_file_location("aaptakosha_content", ROOT / "api" / "content.py")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    assert len(module.PADARTHA_FILES) == 16
    assert set(module.PADARTHA_FILES) == {f"y1-pv-{i}" for i in range(1,17)}
    source = (ROOT / "api" / "curriculum_content.py").read_text(encoding="utf-8")
    assert 'CONTENT_STANDARD_VERSION' in source
    assert 'content_schema_validation_failed' in source