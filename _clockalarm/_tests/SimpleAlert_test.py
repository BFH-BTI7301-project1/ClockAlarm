from _clockalarm import Notification
from _clockalarm.SimpleAlert import SimpleAlert

notification = Notification("Test")


def test_simple_alert_constructor():
    """Test the :class:`~_clockalarm.SimpleAlert` constructor."""
    global notification
    simplealert = SimpleAlert(10, notification)

    assert simplealert.trigger_time == 10
    assert not simplealert.periodicity


def test_get_periodicity():
    """Test the :class:`~_clockalarm.SimpleAlert.get_periodicity` method."""
    global notification
    simplealert = SimpleAlert(10, notification, 30)

    assert simplealert.get_periodicity() == 30


def test_get_notification():
    """Test the :class:`~_clockalarm.SimpleAlert.get_notification` method."""
    global notification
    simplealert = SimpleAlert(10, notification)

    assert (simplealert.get_notification().get_message() ==
            notification.get_message())


def test_simple_alert_triggered(qtbot):
    """Test the :class:`~_clockalarm.SimpleAlert.triggered` method."""
    global notification
    simplealert = SimpleAlert(10, notification)
    with qtbot.waitSignal(simplealert.timeout, raising=True, timeout=1000):
        simplealert.triggered()
