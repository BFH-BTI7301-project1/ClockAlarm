import os
from os.path import join, dirname, abspath

import pytest

from _clockalarm.AlertCollection import AlertCollection
from _clockalarm.utils import importExportUtils
from _clockalarm import SimpleAlert, Notification

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
