"""Universal AaptaKosha learning-content contract and Markdown validator."""
from __future__ import annotations
import re
from dataclasses import dataclass
from typing import Mapping
CONTENT_STANDARD_VERSION = "2.0"
REQUIRED_COMPONENTS = ("learning_objectives","core_notes","tables","mcqs","exam_zone","quick_revision","flashcards","references")
HEADING_ALIASES = {
 "learning_objectives": ("learning objectives",),
 "core_notes": ("meaning","definition","core concepts","explanation"),
 "tables": ("table","comparison"),
 "mcqs": ("mcq","multiple choice","self-assessment"),
 "exam_zone": ("exam","examination","long-answer","short-answer"),
 "quick_revision": ("quick revision","revision"),
 "flashcards": ("flashcard","flash cards","active recall cards"),
 "references": ("references","suggested classical reading","bibliography"),
}
@dataclass(frozen=True)
class ContentValidation:
 valid: bool
 components: Mapping[str,bool]
 errors: tuple[str,...]
 warnings: tuple[str,...] = ()
def _headings(markdown: str) -> list[str]:
 return [m.group(2).strip().lower() for m in re.finditer(r"^(#{1,4})\s+(.+)$", markdown or "", re.M)]
def validate_markdown(markdown: str, *, require_source_text: bool=False) -> ContentValidation:
 text=markdown or ""
 headings=_headings(text)
 components={}
 for key in REQUIRED_COMPONENTS:
  components[key]=any(any(alias in h for alias in HEADING_ALIASES[key]) for h in headings)
 components["tables"]=components["tables"] or bool(re.search(r"^\|.+\|\s*$", text, re.M))
 errors=[f"missing required component: {key}" for key,present in components.items() if not present]
 if require_source_text and not re.search(r"[॥।]", text): errors.append("missing classical Sanskrit source text")
 warnings=[]
 if "```" not in text: warnings.append("no fenced visual/diagram block found; add one when the topic benefits from a visual")
 return ContentValidation(not errors,components,tuple(errors),tuple(warnings))
def assert_publishable(markdown: str, *, require_source_text: bool=False) -> None:
 result=validate_markdown(markdown,require_source_text=require_source_text)
 if not result.valid: raise ValueError("content publication blocked: "+"; ".join(result.errors))
