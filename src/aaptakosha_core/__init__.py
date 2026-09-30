"""AaptaKosha product-domain contracts.

This package contains framework-agnostic domain types that sit above the
Phase 1 ingestion/reconciliation engine.
"""

from .catalog import Curriculum, Subject, Topic

__all__ = ["Curriculum", "Subject", "Topic"]
