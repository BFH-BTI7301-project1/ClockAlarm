import pytest
from os.path import dirname, abspath, join


from PyQt5.QtWidgets import QApplication, QAbstractItemView
from _clockalarm.AlertCollection import AlertCollection
from _clockalarm.UI.AlertListWidget import AlertListWidget
from _clockalarm.utils import importExportUtils


@pytest.fixture
def init_paths(scope="module"):
    importExportUtils.DEFAULT_CONFIG_PATH = join(dirname(abspath(__file__)),
                                                 "config_test.cfg")
    importExportUtils.ALERT_DB_PATH = join(dirname(abspath(__file__)),
                                           "alertsDB_test.json")


app = QApplication([])


@pytest.mark.test
def test_constructor():
    """Test the :class:`~_clockalarm.UI.AlertListWidget` constructor without an
    alert list.
    """
    alw = AlertListWidget()

    assert alw.columnCount() == 4
    assert alw.horizontalHeaderItem(0).text() == 'ID'
    assert alw.horizontalHeaderItem(1).text() == 'Time'
    assert alw.horizontalHeaderItem(2).text() == 'Periodicity'
    assert alw.horizontalHeaderItem(3).text() == 'Message'
    assert not alw.verticalHeader().isVisible()
    assert alw.horizontalHeader().stretchLastSection()
    assert alw.selectionBehavior() == QAbstractItemView.SelectRows
    assert alw.editTriggers() == QAbstractItemView.NoEditTriggers


@pytest.mark.test
def test_constructor_with_alert_list(init_paths):
    """Test the :class:`~_clockalarm.UI.AlertListWidget` constructor with§ an
    alert list.

    Also tests the :class:`~_clockalarm.UI.AlertListWidget.actualize` method.
    """
    global app
    app.alert_collection = AlertCollection()
    app.alert_list = app.alert_collection.alert_list
    app.alw = AlertListWidget()

    assert len(app.alert_collection.alert_list) == 4
    app.alw.actualize(app.alert_collection.alert_list)
    assert app.alw.rowCount() == 4

    # Do not forget to close the db
    app.alert_collection.db.close()
