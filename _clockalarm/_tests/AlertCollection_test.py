import pytest


@pytest.fixture(scope='module')
def before():
    return


@pytest.mark.test
def test_alert_collection_constructor():
    """Test the :class:`~_clockalarm.AllertCollection` constructor.

    Test the correctness of the variable initialization.

    """
