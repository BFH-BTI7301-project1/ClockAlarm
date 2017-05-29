from os.path import dirname, abspath, join

import pytest

from _clockalarm import main, NotificationCenter, Clock, AlertCollection
from _clockalarm.UI import MainWindow
from _clockalarm.utils import importExportUtils

test_config_path = join(dirname(abspath(__file__)), "config_test.cfg")
test_alertsDB_path = join(dirname(abspath(__file__)), "alertsDB_test.json")


@pytest.fixture
def init_paths():
    importExportUtils.DEFAULT_CONFIG_PATH = join(dirname(abspath(__file__)), "config_test.cfg")
    importExportUtils.ALERT_DB_PATH = join(dirname(abspath(__file__)), "alertsDB_test.json")


def test_app_constructor_corrupted_argument():
    """Tests the :class:`~_clockalarm.main.App` constructor with corrupted files.

    """
    with pytest.raises(ValueError):
        argv = ["file", "corrupted/file/path", test_alertsDB_path]
        main.App(argv[1], argv[2], argv)
    with pytest.raises(ValueError):
        argv = ["file", test_config_path, "corrupted/file/path"]
        main.App(argv[1], argv[2], argv)


def test_app_constructor_nonexistent_argument():
    """Tests the :class:`~_clockalarm.main.App` constructor with nonexistent files.

    """
    with pytest.raises(ValueError):
        argv = ["file", "nonexistent/file/path.json", test_alertsDB_path]
        main.App(argv[1], argv[2], argv)
    with pytest.raises(ValueError):
        argv = ["file", test_config_path, "nonexistent/file/path.cfg"]
        main.App(argv[1], argv[2], argv)


def test_app_constructor():
    """Tests the :class:`~_clockalarm.main.App` constructor.

    """
    argv = ["file", test_config_path, test_alertsDB_path]
    app = main.App(argv[1], argv[2], argv)

    assert app.CLOCK_FREQUENCY == importExportUtils.get_default_config("CLOCK_FREQUENCY", "int")
    assert app.MUTE == importExportUtils.get_default_config("MUTE", "bool")
    assert isinstance(app.main_window, MainWindow.MainWindow)
    assert isinstance(app.notification_center, NotificationCenter.NotificationCenter)
    assert isinstance(app.clock_thread, Clock)
    assert app.alert_collection is None  # alert_collection is not initializes in constructor

    app.init_alert_collection()
    assert isinstance(app.alert_collection, AlertCollection.AlertCollection)

    app.clock_thread.stop()
    app.alert_collection.db.close()
