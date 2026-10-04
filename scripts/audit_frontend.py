from __future__ import annotations

from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urlsplit

ROOT = Path(__file__).resolve().parents[1] / "frontend"
HTML_FILES = sorted(ROOT.rglob("*.html"))
GLYPHS = "✦⌂▱❋◇□⌁▤♡•••☘◒♧⌕⌄"

class AuditParser(HTMLParser):
    def __init__(self, path: Path):
        super().__init__(convert_charrefs=True)
        self.path = path
        self.links: list[str] = []
        self.inputs: list[tuple[dict[str, str], int]] = []
        self.labels: list[dict[str, str]] = []
        self.nav_depth = 0
        self.nav_hrefs: list[str] = []
        self.current_anchor: dict[str, str] | None = None
        self.anchor_text = ""
        self.anchor_hidden_depth = 0
        self.raw_glyph_anchors: list[tuple[int, str]] = []

    def handle_starttag(self, tag, attrs):
        data = dict(attrs)
        if tag == "a" and data.get("href"):
            self.links.append(data["href"])
            if self.nav_depth:
                self.nav_hrefs.append(data["href"])
            self.current_anchor = data
            self.anchor_text = ""
        elif tag == "input":
            self.inputs.append((data, self.getpos()[0]))
        elif tag == "label":
            self.labels.append(data)
        elif tag == "nav":
            self.nav_depth += 1
        elif self.current_anchor is not None and data.get("aria-hidden") == "true":
            self.anchor_hidden_depth += 1
        elif tag == "script" and data.get("src"):
            self.links.append(data["src"])

    def handle_endtag(self, tag):
        if tag == "a" and self.current_anchor is not None:
            text = self.anchor_text.strip()
            if self.anchor_hidden_depth == 0 and any(g in text for g in GLYPHS):
                self.raw_glyph_anchors.append((self.getpos()[0], text))
            self.current_anchor = None
            self.anchor_text = ""
            self.anchor_hidden_depth = 0
        elif tag == "nav":
            self.nav_depth = max(0, self.nav_depth - 1)

    def handle_data(self, data):
        if self.current_anchor is not None:
            self.anchor_text += data

def resolve_target(source: Path, href: str) -> Path | None:
    parsed = urlsplit(href)
    if parsed.scheme or parsed.netloc:
        return None
    path = parsed.path
    if not path or path.startswith("/api/"):
        return None
    target = (source.parent / path).resolve()
    try:
        target.relative_to(ROOT.resolve())
    except ValueError:
        return None
    if target.suffix == "":
        target = target / "index.html"
    return target

errors: list[str] = []
index = ROOT / "index.html"
if index.exists():
    index_text = index.read_text(encoding="utf-8")
    required_mobile_routes = ["./curriculum.html", "./samhita.html", "./practice.html", "./more.html"]
    bottom_nav_start = index_text.find('<nav class="bottom-nav"')
    bottom_nav_end = index_text.find("</nav>", bottom_nav_start)
    bottom_nav = index_text[bottom_nav_start:bottom_nav_end] if bottom_nav_start >= 0 else ""
    for route in required_mobile_routes:
        if route not in bottom_nav:
            errors.append(f"index.html -> mobile navigation missing {route}")

for html in HTML_FILES:
    parser = AuditParser(html)
    parser.feed(html.read_text(encoding="utf-8"))
    for href in parser.links:
        target = resolve_target(html, href)
        if target is not None and not target.exists():
            errors.append(f"{html.relative_to(ROOT)} -> missing target {href}")
    for attrs, line in parser.inputs:
        input_type = attrs.get("type", "text")
        if input_type in {"hidden", "submit", "button", "reset", "checkbox", "radio", "file"}:
            continue
        if not attrs.get("aria-label") and not attrs.get("aria-labelledby") and not attrs.get("id"):
            errors.append(f"{html.relative_to(ROOT)}:{line} -> form control needs aria-label/aria-labelledby or id")
    if parser.raw_glyph_anchors:
        for line, text in parser.raw_glyph_anchors:
            errors.append(f"{html.relative_to(ROOT)}:{line} -> navigation icon text must be wrapped in aria-hidden span: {text!r}")

    # Catch accidental duplicate navigation destinations on the same nav.
    duplicates = {href for href in parser.nav_hrefs if parser.nav_hrefs.count(href) > 1}
    for href in sorted(duplicates):
        errors.append(f"{html.relative_to(ROOT)} -> duplicate navigation href {href}")

if errors:
    print("\n".join(errors))
    raise SystemExit(1)

print(f"Frontend audit passed: {len(HTML_FILES)} HTML files checked.")
