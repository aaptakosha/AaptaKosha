from html.parser import HTMLParser
from pathlib import Path
import subprocess, sys
ROOT=Path(__file__).resolve().parents[1]
errors=[]
class Parser(HTMLParser):
    def __init__(self,path): super().__init__(); self.path=path; self.ids=set(); self.links=[]
    def handle_starttag(self,tag,attrs):
        a=dict(attrs)
        if 'id' in a:
            if a['id'] in self.ids: errors.append(f"{self.path}: duplicate id #{a['id']}")
            self.ids.add(a['id'])
        if tag in ('a','link') and a.get('href'): self.links.append(a['href'])
        if tag=='script' and a.get('src'): self.links.append(a['src'])
        if tag=='img' and 'alt' not in a: errors.append(f"{self.path}: image missing alt")
html_files=list((ROOT/'frontend').glob('*.html')); parsers={}; all_ids={}
for p in html_files:
    parser=Parser(p.relative_to(ROOT))
    try: parser.feed(p.read_text(encoding='utf-8'))
    except Exception as e: errors.append(f"{p.relative_to(ROOT)}: HTML parse error: {e}")
    parsers[p.name]=parser; all_ids[p.name]=parser.ids
for p in html_files:
    parser=parsers[p.name]
    for href in parser.links:
        if href.startswith('#'):
            if href[1:] and href[1:] not in parser.ids: errors.append(f"{p.relative_to(ROOT)}: missing local anchor {href}")
        elif href.startswith('./') and '#' in href:
            target,frag=href[2:].split('#',1); ids=all_ids.get(target)
            if ids is not None and frag and frag not in ids: errors.append(f"{p.relative_to(ROOT)}: missing target anchor {href}")
for p in (ROOT/'frontend').glob('*.js'):
    try:
        r=subprocess.run(['node','--check',str(p)],capture_output=True,text=True)
        if r.returncode: errors.append(f"{p.relative_to(ROOT)}: JS syntax error: {r.stderr.strip()}")
    except FileNotFoundError: pass
for p in (ROOT/'frontend').glob('*.css'):
    if p.read_text(encoding='utf-8').count('{')!=p.read_text(encoding='utf-8').count('}'): errors.append(f"{p.relative_to(ROOT)}: unbalanced CSS braces")
if errors: print("\\n".join(errors)); sys.exit(1)
print(f"Validated {len(html_files)} HTML files, frontend JS syntax, and CSS brace balance.")
