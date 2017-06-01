import pytest

from _clockalarm.Alert import Alert

alert = Alert(3)


@pytest.mark.test
def test_alert_constructor():
    """Test the :class:`~_clockalarm.Alert` constructor."""
    global alert
    assert alert.trigger_time == 3
    assert not alert.id


@pytest.mark.test
def test_get_id():
    """Test the :class:`~_clockalarm.Alert.get_id` method."""
    global alert
    assert not alert.get_id()


@pytest.mark.test
def test_get_trigger_time():
    """Test the :class:`~_clockalarm.Alert.get_trigger_time` method."""
    global alert
    assert alert.get_trigger_time() == 3


@pytest.mark.test
def test_triggered():
    """Cannot test the :class:`~_clockalarm.Alert.triggered` method."""
    pass
