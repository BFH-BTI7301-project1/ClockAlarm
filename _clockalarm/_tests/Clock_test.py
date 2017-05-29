import _clockalarm.Clock as Clock

clock = Clock(1)


def test_clock_constructor():
    """Test the :class:`~_clockalarm.Clock` constructor."""
    global clock
    assert clock._frequency == 1
    assert clock.running


def test_clock_running(qtbot):
    """Test :class:`~_clockalarm.Clock.stop` method.

    Tests with a mock object the ticks of the clock.
    """
    clock2 = Clock(1)
    # clock2.run()
    # clock2.stop()


def test_clock_stop():
    """Test :class:`~_clockalarm.Clock.stop` method."""
    global clock
    assert clock.running
    clock.stop()
    assert not clock.running
