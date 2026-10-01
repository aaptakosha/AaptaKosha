import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / "content/samhita/charaka/sutrasthana"

def test_chapters_1_to_12_have_real_verse_specific_tika():
    for number in range(1, 13):
        path = BASE / f"adhyaya-{number:02d}.json"
        chapter = json.loads(path.read_text(encoding="utf-8"))
        verses = chapter["verses"]
        values = [v["tika_hi"].strip() for v in verses]
        assert all(values), f"empty tika in chapter {number}"
        assert not any("मूल-पाठ आधारित शैक्षिक सारांश" in v for v in values), f"placeholder in chapter {number}"
        assert not any(v == "अध्ययन-सार: श्लोक" + str(i) + " के मुख्य पदों को मूल पाठ के साथ दोहराएँ।" for i, v in enumerate(values, 1)), f"legacy placeholder in chapter {number}"
        assert len(set(values)) >= max(1, int(len(values) * 0.95)), f"repeated tika in chapter {number}"
        assert all(len(v) >= 60 for v in values), f"tika too short in chapter {number}"
