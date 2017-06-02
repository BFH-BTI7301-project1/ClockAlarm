import pytest
from os.path import dirname, abspath, join


from PyQt5.QtWidgets import QApplication, QGroupBox, QTimeEdit, \
        QDateTimeEdit
from _clockalarm.UI.SimpleAlertEditWidget import SimpleAlertEditWidget
from _clockalarm.utils import importExportUtils


@pytest.fixture
def init_paths(scope="module"):
    importExportUtils.DEFAULT_CONFIG_PATH = join(dirname(abspath(__file__)),
                                                 "config_test.cfg")
    importExportUtils.ALERT_DB_PATH = join(dirname(abspath(__file__)),
                                           "alertsDB_test.json")


app = QApplication([])


@pytest.mark.test
def test_constructor_without_alert():
    """Test the :class:`~_clockalarm.UI.SimpleAlertEditWidget` constructor
    without an alert.
    """

    saew = SimpleAlertEditWidget()

    group_box = saew.findChildren(QGroupBox)[0]
    periodicity_edit = saew.findChildren(QTimeEdit)[0]

    assert group_box.title() == 'Set up a new Simple Alert'
    assert periodicity_edit.displayFormat() == 'HH:mm:ss'
    assert periodicity_edit.time().toString() == '00:00:00'

    print(periodicity_edit.displayFormat())

    assert isinstance(saew.date_time_edit, QDateTimeEdit)


@pytest.mark.test
def test_constructor_with_alert_list(init_paths):
    """Test the :class:`~_clockalarm.UI.AlertListWidget` constructor with an
    alert list.
    """
    pass
