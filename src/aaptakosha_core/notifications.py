"""Framework-neutral notification and automation contracts."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Mapping, Protocol, Tuple


@dataclass(frozen=True, slots=True)
class Notification:
    """A provider-neutral message ready for delivery."""

    notification_id: str
    recipient_id: str
    event_type: str
    title: str
    body: str
    channel: str = "in_app"
    metadata: Tuple[Tuple[str, str], ...] = ()

    def __post_init__(self) -> None:
        for value, field in (
            (self.notification_id, "notification_id"),
            (self.recipient_id, "recipient_id"),
            (self.event_type, "event_type"),
            (self.title, "title"),
            (self.body, "body"),
            (self.channel, "channel"),
        ):
            if not value.strip():
                raise ValueError(f"{field} must not be empty")


class NotificationSender(Protocol):
    """Adapter boundary for an external or internal delivery provider."""

    def send(self, notification: Notification) -> None: ...


class NotificationRepository(Protocol):
    """Persistence boundary for queued notification records."""

    def enqueue(self, notification: Notification) -> None: ...

    def list_pending(self, limit: int = 100) -> Tuple[Notification, ...]: ...

    def mark_sent(self, notification_id: str) -> None: ...


@dataclass(frozen=True, slots=True)
class AutomationRule:
    """Declarative event-to-notification rule."""

    event_type: str
    channel: str
    title_template: str
    body_template: str

    def __post_init__(self) -> None:
        for value, field in (
            (self.event_type, "event_type"),
            (self.channel, "channel"),
            (self.title_template, "title_template"),
            (self.body_template, "body_template"),
        ):
            if not value.strip():
                raise ValueError(f"{field} must not be empty")


class NotificationService:
    """Create and queue notifications without knowing delivery providers."""

    def __init__(self, repository: NotificationRepository):
        self.repository = repository

    def queue(self, notification: Notification) -> Notification:
        self.repository.enqueue(notification)
        return notification

    def from_rule(
        self,
        rule: AutomationRule,
        notification_id: str,
        recipient_id: str,
        context: Mapping[str, str],
    ) -> Notification:
        notification = Notification(
            notification_id=notification_id,
            recipient_id=recipient_id,
            event_type=rule.event_type,
            title=rule.title_template.format_map(context),
            body=rule.body_template.format_map(context),
            channel=rule.channel,
            metadata=tuple(sorted((str(k), str(v)) for k, v in context.items())),
        )
        return self.queue(notification)


class NotificationDispatcher:
    """Deliver pending notifications and mark successful sends."""

    def __init__(
        self,
        repository: NotificationRepository,
        senders: Mapping[str, NotificationSender],
    ):
        self.repository = repository
        self.senders = dict(senders)

    def dispatch(self, limit: int = 100) -> int:
        if limit < 1:
            raise ValueError("limit must be >= 1")
        delivered = 0
        for notification in self.repository.list_pending(limit):
            sender = self.senders.get(notification.channel)
            if sender is None:
                continue
            sender.send(notification)
            self.repository.mark_sent(notification.notification_id)
            delivered += 1
        return delivered


__all__ = [
    "AutomationRule",
    "Notification",
    "NotificationDispatcher",
    "NotificationRepository",
    "NotificationSender",
    "NotificationService",
]
