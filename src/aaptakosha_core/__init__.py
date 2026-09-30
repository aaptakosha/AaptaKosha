"""AaptaKosha product-domain contracts, services, persistence, and authorization."""
from .api import CatalogApi
from .auth import (
    AuthorizationDeniedError,
    AuthorizationService,
    CATALOG_ADMIN,
    CATALOG_READ,
    Principal,
)
from .catalog import Curriculum, Subject, Topic
from .notifications import (
    AutomationRule,
    Notification,
    NotificationDispatcher,
    NotificationRepository,
    NotificationSender,
    NotificationService,
)
from .progress import (
    COMPLETED,
    IN_PROGRESS,
    NOT_STARTED,
    LearningProgress,
    LearningProgressRepository,
    LearningProgressService,
)
from .services import CatalogNotFoundError, CatalogRepository, CatalogService
from .sqlite_repository import SQLiteCatalogRepository

__all__ = [
    "AuthorizationDeniedError",
    "AuthorizationService",
    "CATALOG_ADMIN",
    "CATALOG_READ",
    "CatalogApi",
    "CatalogNotFoundError",
    "CatalogRepository",
    "CatalogService",
    "AutomationRule",
    "COMPLETED",
    "IN_PROGRESS",
    "NOT_STARTED",
    "Curriculum",
    "LearningProgress",
    "LearningProgressRepository",
    "LearningProgressService",
    "Notification",
    "NotificationDispatcher",
    "NotificationRepository",
    "NotificationSender",
    "NotificationService",
    "Principal",
    "Subject",
    "Topic",
    "SQLiteCatalogRepository",
]
