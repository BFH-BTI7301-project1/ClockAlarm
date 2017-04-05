from _clockalarm import Notification


def test_notification():
    notification = Notification("Test")

    assert notification.message == "Test"
