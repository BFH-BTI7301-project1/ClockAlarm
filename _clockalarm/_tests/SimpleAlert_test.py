from _clockalarm.SimpleAlert import SimpleAlert
from _clockalarm import Notification


def test_simple_alert_constructor():
    """Test the :class:`~_clockalarm.SimpleAlert` constructor."""
    notification = Notification("Test")
    simplealert = SimpleAlert(10, notification)

    assert simplealert.trigger_time == 10
    assert simplealert.notification.get_message() == "Test"
    assert not simplealert.periodicity


def test_simple_alert_triggered():
    """Test the :class:`~_clockalarm.SimpleAlert.triggered` method."""
    pass


def test_get_identifier():
    """Test the :class:`~_clockalarm.SimpleAlert.get_identifier` method."""
    pass
