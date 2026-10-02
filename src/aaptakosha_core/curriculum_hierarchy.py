"""NCISM curriculum hierarchy read models and repository boundary."""
from __future__ import annotations

from typing import Protocol, Tuple

from .catalog import CurriculumNode


class CurriculumHierarchyRepository(Protocol):
    def list_nodes(
        self,
        curriculum_id: str,
        subject_id: str | None = None,
        version: str | None = None,
        parent_node_id: str | None = None,
    ) -> Tuple[CurriculumNode, ...]: ...

    def get_node(
        self,
        node_id: str,
        curriculum_id: str | None = None,
        version: str | None = None,
    ) -> CurriculumNode | None: ...
