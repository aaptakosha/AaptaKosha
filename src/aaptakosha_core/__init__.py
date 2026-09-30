"""AaptaKosha product-domain contracts, services, and persistence adapters."""
from .catalog import Curriculum, Subject, Topic
from .services import CatalogNotFoundError, CatalogRepository, CatalogService
from .sqlite_repository import SQLiteCatalogRepository

__all__ = [
    "CatalogNotFoundError",
    "CatalogRepository",
    "CatalogService",
    "Curriculum",
    "Subject",
    "Topic",
    "SQLiteCatalogRepository",
]
