"""AaptaKosha product-domain contracts, services, and persistence adapters."""
from .catalog import Curriculum, Subject, Topic
from .api import CatalogApi
from .services import CatalogNotFoundError, CatalogRepository, CatalogService
from .sqlite_repository import SQLiteCatalogRepository

__all__ = [
    "CatalogApi",
    "CatalogNotFoundError",
    "CatalogRepository",
    "CatalogService",
    "Curriculum",
    "Subject",
    "Topic",
    "SQLiteCatalogRepository",
]
