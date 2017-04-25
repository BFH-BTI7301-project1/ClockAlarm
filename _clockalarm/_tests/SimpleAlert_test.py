from _clockalarm import SimpleAlert


def test_simple_alert_constructor():
    """Test the :class:`~_clockalarm.SimpleAlert` constructor."""
    simplealert = SimpleAlert(10, "Test")

    assert simplealert.trigger_time == 10
    assert simplealert._notification.message == "Test"


def test_simple_alert_triggered():
    """Test the :class:`~_clockalarm.SimpleAlert.triggered` method."""
    pass


def test_get_identifier():
    """Test the :class:`~_clockalarm.SimpleAlert.get_identifier` method."""
    simplealert = SimpleAlert(10, "Test")

    assert simplealert.get_identifier() == "Test"
