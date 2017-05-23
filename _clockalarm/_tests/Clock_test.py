import _clockalarm.Clock as Clock


def test_clock_constructor():
    """Test the :class:`~_clockalarm.Clock` constructor."""
    clock = Clock(1)
    assert clock._frequency == 1
    assert clock.running


def test_clock_running():
    """Test :class:`~_clockalarm.Clock.stop` method.

    Tests with a mock object the ticks of the clock.
    """
    pass


def test_clock_stop():
    """Test :class:`~_clockalarm.Clock.stop` method."""
    clock = Clock(1)
    assert clock.running
    clock.stop()
    assert not clock.running
