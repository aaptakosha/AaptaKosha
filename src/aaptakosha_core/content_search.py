"""Framework-neutral search/indexing boundary for content."""
from __future__ import annotations
from dataclasses import dataclass
from typing import Protocol, Tuple
from .content import ContentResource, PUBLISHED

@dataclass(frozen=True, slots=True)
class ContentSearchResult:
    resource_id: str
    title: str
    resource_type: str
    score: float

class ContentSearchIndex(Protocol):
    def index(self, resource: ContentResource) -> None: ...
    def remove(self, resource_id: str) -> None: ...
    def search(self, query: str, limit: int = 20) -> Tuple[ContentSearchResult, ...]: ...

class InMemoryContentSearchIndex:
    """Deterministic reference index; replaceable by a production search adapter."""
    def __init__(self): self._resources: dict[str, ContentResource] = {}
    def index(self, resource: ContentResource) -> None:
        if resource.status == PUBLISHED: self._resources[resource.resource_id] = resource
        else: self._resources.pop(resource.resource_id, None)
    def remove(self, resource_id: str) -> None: self._resources.pop(resource_id, None)
    def search(self, query: str, limit: int = 20):
        if not query.strip() or limit < 1: return ()
        terms=tuple(query.lower().split()); results=[]
        for r in self._resources.values():
            haystack=f"{r.title} {r.summary} {r.resource_type} {' '.join(r.curriculum_refs)}".lower()
            score=sum(haystack.count(term) for term in terms)
            if score: results.append(ContentSearchResult(r.resource_id,r.title,r.resource_type,float(score)))
        return tuple(sorted(results,key=lambda x:(-x.score,x.resource_id))[:limit])

__all__=["ContentSearchIndex","ContentSearchResult","InMemoryContentSearchIndex"]
