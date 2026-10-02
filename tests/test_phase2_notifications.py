import pytest

from aaptakosha_core.notifications import (
    AutomationRule,
    Notification,
    NotificationDispatcher,
    NotificationService,
)


class InMemoryNotifications:
    def __init__(self):
        self.pending = []
        self.sent = []

    def enqueue(self, notification):
        self.pending.append(notification)

    def list_pending(self, limit=100):
        return tuple(self.pending[:limit])

    def mark_sent(self, notification_id):
        self.pending = [n for n in self.pending if n.notification_id != notification_id]
        self.sent.append(notification_id)


class Sender:
    def __init__(self):
        self.received = []

    def send(self, notification):
        self.received.append(notification)


def test_rule_creates_and_queues_notification():
    repo = InMemoryNotifications()
    service = NotificationService(repo)
    rule = AutomationRule(
        "progress.completed",
        "in_app",
        "Completed: {resource}",
        "You completed {resource}.",
    )

    notification = service.from_rule(
        rule, "n-1", "user-1", {"resource": "Rasa"}
    )

    assert notification.title == "Completed: Rasa"
    assert repo.pending == [notification]


def test_dispatcher_uses_channel_adapter_and_marks_sent():
    repo = InMemoryNotifications()
    service = NotificationService(repo)
    service.queue(Notification("n-1", "user-1", "test", "Title", "Body"))
    sender = Sender()

    delivered = NotificationDispatcher(repo, {"in_app": sender}).dispatch()

    assert delivered == 1
    assert sender.received[0].notification_id == "n-1"
    assert repo.sent == ["n-1"]


def test_unknown_channel_remains_pending():
    repo = InMemoryNotifications()
    repo.enqueue(Notification("n-1", "user-1", "test", "Title", "Body", "push"))

    delivered = NotificationDispatcher(repo, {"in_app": Sender()}).dispatch()

    assert delivered == 0
    assert len(repo.pending) == 1


def test_dispatch_limit_must_be_positive():
    with pytest.raises(ValueError):
        NotificationDispatcher(InMemoryNotifications(), {}).dispatch(0)
