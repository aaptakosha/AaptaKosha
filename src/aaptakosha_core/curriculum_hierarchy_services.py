"""Application service for navigating the NCISM curriculum tree."""
from __future__ import annotations

from dataclasses import dataclass
from typing import Tuple

from .catalog import CurriculumNode
from .curriculum_hierarchy import CurriculumHierarchyRepository


class CurriculumHierarchyNotFoundError(LookupError):
    """Raised when a requested curriculum hierarchy node does not exist."""


@dataclass(frozen=True, slots=True)
class CurriculumHierarchyService:
    repository: CurriculumHierarchyRepository

    def list_nodes(
        self,
        curriculum_id: str,
        subject_id: str | None = None,
        version: str | None = None,
        parent_node_id: str | None = None,
    ) -> Tuple[CurriculumNode, ...]:
        return self.repository.list_nodes(curriculum_id, subject_id, version, parent_node_id)

    def get_node(
        self,
        node_id: str,
        curriculum_id: str | None = None,
        version: str | None = None,
    ) -> CurriculumNode:
        node = self.repository.get_node(node_id, curriculum_id, version)
        if node is None:
            raise CurriculumHierarchyNotFoundError("curriculum node not found: " + node_id)
        return node

    def children(
        self,
        curriculum_id: str,
        parent_node_id: str | None = None,
        subject_id: str | None = None,
        version: str | None = None,
    ) -> Tuple[CurriculumNode, ...]:
        return self.list_nodes(curriculum_id, subject_id, version, parent_node_id)


__all__ = ["CurriculumHierarchyNotFoundError", "CurriculumHierarchyService"]
