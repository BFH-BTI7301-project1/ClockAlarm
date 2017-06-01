import pytest

import time
import _clockalarm.Clock as Clock

clock = Clock(1)


@pytest.mark.test
def test_clock_constructor():
    """Test the :class:`~_clockalarm.Clock` constructor."""
    global clock
    assert clock._frequency == 1
    assert clock.running


@pytest.mark.test
def test_clock_running(qtbot):
    """Test :class:`~_clockalarm.Clock.run` method."""
    clock2 = Clock(1)
    with qtbot.waitSignal(clock2.tick, raising=True):
        clock2.start()
        time.sleep(1)
        clock2.stop()


@pytest.mark.test
def test_clock_stop():
    """Test :class:`~_clockalarm.Clock.stop` method."""
    global clock
    assert clock.running
    clock.stop()
    assert not clock.running
