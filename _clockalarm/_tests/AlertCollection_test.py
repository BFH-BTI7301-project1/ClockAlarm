import os
import time
from os.path import join, dirname, abspath

import pytest

from _clockalarm import SimpleAlert, Notification
from _clockalarm.AlertCollection import AlertCollection
from _clockalarm.utils import importExportUtils

test_config_path = join(dirname(abspath(__file__)), "config_test.cfg")
test_alertsDB_path = join(dirname(abspath(__file__)), "alertsDB_test.json")


@pytest.fixture(scope='module')
def before():
    importExportUtils.DEFAULT_CONFIG_PATH = test_config_path
    importExportUtils.ALERT_DB_PATH = test_alertsDB_path


@pytest.mark.test
def test_alert_collection_constructor(before):
    """Test the :class:`~_clockalarm.AllertCollection` constructor.

    Test the correctness of the variable initialization.

    """
    alert_collection = AlertCollection()

    assert isinstance(alert_collection, AlertCollection)
    assert alert_collection.parent is None

    alert_collection.db.close()


@pytest.mark.test
def test_alert_collection_constructor_new_db(before):
    """Test the :class:`~_clockalarm.AllertCollection` constructor.

    Build AlertCollection object with a nonexistent db path create the db.

    """
    importExportUtils.ALERT_DB_PATH = join(dirname(abspath(__file__)), "new_alertsDB_test.json")  # new db path
    alert_collection = AlertCollection()
    alert_collection.db.close()

    assert os.path.isfile(importExportUtils.ALERT_DB_PATH)

    os.remove(importExportUtils.ALERT_DB_PATH)  # remove the new db
    importExportUtils.ALERT_DB_PATH = test_alertsDB_path


@pytest.mark.test
def test_alert_collection_constructor_wrong_parent(before):
    """Test the :class:`~_clockalarm.AllertCollection` constructor.

    Build AlertCollection object with a wrong parent argument

    """
    with pytest.raises(ValueError):
        AlertCollection("str argument")


@pytest.mark.test
def test_alert_collection_add_wrong_argument(before):
    """Test the :class:`~_clockalarm.AllertCollection` add method.

    Incorrect argument passed tho add.

    """
    alert_collection = AlertCollection()
    with pytest.raises(ValueError):
        alert_collection.add(None)
    with pytest.raises(ValueError):
        alert_collection.add('not a SimpleAlert')

    alert_collection.db.close()


@pytest.mark.test
def test_alert_collection_add(before):
    """Test the :class:`~_clockalarm.AllertCollection` add method."""
    alert_collection = AlertCollection()
    alert = SimpleAlert.SimpleAlert(10, Notification('test message'))
    assert not alert.id
    alert_collection.add(alert)

    assert alert in alert_collection.alert_list
    assert alert.id
    alert_collection.alert_list.remove(alert)

    alert_collection.db.close()


@pytest.mark.test
def test_alert_collection_edit_nonexistent_alert(before):
    """Test the :class:`~_clockalarm.AllertCollection` edit method.

    The alert to modify isn't in the database.

    """
    alert_collection = AlertCollection()
    with pytest.raises(KeyError):
        alert_collection.edit(-1)

    alert_collection.db.close()


@pytest.mark.test
def test_alert_collection_edit_wrong_argument(before):
    """Test the :class:`~_clockalarm.AllertCollection` edit method.

    The element to change are wrong

    """
    alert_collection = AlertCollection()
    with pytest.raises(ValueError):
        alert_collection.edit(2, periodicity=0)
    with pytest.raises(ValueError):
        alert_collection.edit(2, trigger_time=10)

    alert_collection.db.close()


@pytest.mark.test
def test_alert_collection_edit(before):
    """Test the :class:`~_clockalarm.AllertCollection` edit method."""
    alert_collection = AlertCollection()
    trigger_time = time.time() + 60
    notification = Notification("notification message")
    alert = SimpleAlert.SimpleAlert(trigger_time, notification)

    alert_collection.add(alert)
    notification_2 = Notification("notification message 2")

    alert_collection.edit(alert.id, notification=notification_2, trigger_time=trigger_time + 60, periodicity=60)
    assert alert.trigger_time == trigger_time + 60
    assert alert.periodicity == 60
    assert alert.notification == notification_2

    alert_collection.delete(alert.id)
    alert_collection.db.close()


@pytest.mark.test
def test_alert_collection_delete_nonexistent_id(before):
    """Test the :class:`~_clockalarm.AllertCollection` delete method.

    The alert to delete isn't in the database.

    """
    alert_collection = AlertCollection()
    with pytest.raises(KeyError):
        alert_collection.delete(-1)

    alert_collection.db.close()


@pytest.mark.test
def test_alert_collection_delete(before):
    """Test the :class:`~_clockalarm.AllertCollection` delete method."""
    alert_collection = AlertCollection()
    alert = SimpleAlert.SimpleAlert(10, Notification("notification message"))
    alert_collection.add(alert)

    assert alert in alert_collection.alert_list
    alert_collection.delete(alert.id)
    assert alert not in alert_collection.alert_list

    alert_collection.db.close()


@pytest.mark.test
def test_alert_collection_check_timers(before):
    """Test the :class:`~_clockalarm.AllertCollection` check_timers method."""
    alert_collection = AlertCollection()
    alert = SimpleAlert.SimpleAlert(9, Notification("this notification should be triggered"))
    alert_collection.add(alert)

    assert alert in alert_collection.alert_list
    alert_collection.check_timers(10)
    assert alert not in alert_collection.alert_list

    alert = SimpleAlert.SimpleAlert(11, Notification("this notification shouldn't be triggered"))
    alert_collection.add(alert)

    assert alert in alert_collection.alert_list
    alert_collection.check_timers(10)
    assert alert in alert_collection.alert_list

    alert_collection.delete(alert.id)

    alert_collection.db.close()


@pytest.mark.test
def test_alert_collection_check_timers_with_periodicity(before):
    """Test the :class:`~_clockalarm.AllertCollection` check_timers method."""
    alert_collection = AlertCollection()
    now = time.time()
    alert = SimpleAlert.SimpleAlert(now, Notification("periodic notification"), periodicity=60)
    alert_collection.add(alert)

    assert alert in alert_collection.alert_list
    alert_collection.check_timers(time.time())
    assert alert.trigger_time == now + 60

    alert_collection.delete(alert.id)

    alert_collection.db.close()
