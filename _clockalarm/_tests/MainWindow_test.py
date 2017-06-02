from os.path import join, abspath, dirname

import pytest
from PyQt5 import QtCore
from PyQt5.Qt import QRect
from PyQt5.QtCore import QPoint, QSize
from PyQt5.QtGui import QCloseEvent
from PyQt5.QtWidgets import QAction, QWidget, QGridLayout, QPushButton, QMenu, \
    QSystemTrayIcon

from _clockalarm.Notification import Notification
from _clockalarm.UI.SimpleAlertEditWidget import SimpleAlertEditWidget
from _clockalarm.main import App
from _clockalarm.utils import importExportUtils

alert_db_path = join(dirname(abspath(__file__)), "alertsDB_test.json")
default_config_path = join(dirname(abspath(__file__)), "config_test.cfg")


@pytest.fixture
def init_paths():
    importExportUtils.DEFAULT_CONFIG_PATH = default_config_path
    importExportUtils.ALERT_DB_PATH = alert_db_path


sound_path = join(dirname(dirname(abspath(__file__))), 'resources', 'sounds',
                  'floop.wav')
im_path = join(dirname(dirname(abspath(__file__))), 'resources', 'images',
               'notification_clock.png')

notification = Notification("Test", "000000", "Times", 12, sound_path)
rect = QRect(0, 0, 1024, 768)

# A App is needed for the MainWindow
app = App(default_config_path, alert_db_path, [])
mw = app.main_window


@pytest.mark.test
def test_constructor(init_paths):
    """Test :class:~_clockalarm.UI.MainWindow constructor."""
    global mw

    assert mw.minimumSize() == QSize(300, 100)
    assert mw.windowTitle() == "ClockAlarm Manager"
    assert mw.size() == QSize(800, 400)

    children = mw.findChildren(QAction)

    assert children[0].text() == "Import Alerts File"
    assert children[1].text() == "Export Alerts File"
    assert children[2].text() == "Exit"
    assert children[3].text() == "New Simple Alert"
    assert children[4].text() == "Delete Alert"
    assert children[5].text() == "Edit Alert"

    assert mw.findChildren(QWidget)
    assert mw.findChildren(QGridLayout)
    assert mw.findChildren(QPushButton)
    assert mw.findChildren(QSystemTrayIcon)
    assert mw.findChildren(QMenu)

    assert mw.findChildren(QSystemTrayIcon)[0].isVisible()


@pytest.mark.test
def test_tray_icon_click_test(init_paths, qtbot):
    """Test :class:~_clockalarm.UI.MainWindow.tray_icon_click method."""
    global mw

    mw.hide()
    mw.tray_icon_click(QSystemTrayIcon.DoubleClick)
    assert mw.isVisible()


@pytest.mark.test
def test_mute_buton_click(init_paths, qtbot):
    """Test :class:~_clockalarm.UI.MainWindow.mute_button_click method."""
    global mw

    with qtbot.waitExposed(mw):
        mw.show()

    mute_before_click = importExportUtils.get_default_config('MUTE', 'bool')

    qtbot.mouseMove(mw, mw.mute_pushbutton.pos() + QPoint(10, 10))
    qtbot.mouseClick(mw.mute_pushbutton, QtCore.Qt.LeftButton)

    mute_after_click = importExportUtils.get_default_config('MUTE', 'bool')
    # Need to click again otherwise the some other tests may fail
    qtbot.mouseClick(mw.mute_pushbutton, QtCore.Qt.LeftButton)
    assert mute_before_click != mute_after_click


@pytest.mark.test
def test_closeEvent(init_paths):
    """Test :class:~_clockalarm.UI.MainWindow.closeEvent method."""
    global mw

    mw.show()
    event = QCloseEvent()
    mw.closeEvent(event)
    assert not mw.isVisible()


@pytest.mark.test
def test_add_simple_alert(init_paths):
    """Test :class:~_clockalarm.UI.MainWindow.add_simple_alert method.

    It is too difficult to test the GUI at this point.
    """
    global mw

    print(mw.dialog_widget)
    assert not mw.dialog_widget

    mw.add_simple_alert()
    assert mw.dialog_widget
    assert isinstance(mw.dialog_widget, SimpleAlertEditWidget)
    assert mw.dialog_widget.isVisible()
    mw.dialog_widget.close()
    mw.dialog_widget = None


@pytest.mark.test
def test_edit_simple_alert(init_paths):
    """Test :class:~_clockalarm.UI.MainWindow.edit_simple_alert method.

    It is too difficult to test the GUI at this point.
    """
    global mw

    assert not mw.dialog_widget

    mw.edit_simple_alert()
    assert not mw.dialog_widget


@pytest.mark.test
def test_delete_alerts(init_paths, qtbot):
    """Test :class:~_clockalarm.UI.MainWindow.delete_alerts method.

    It is too difficult to test the GUI at this point.
    """
    global mw
    global app
    app.init_alert_collection()

    assert mw.alert_list_widget.rowCount() == 4
    mw.delete_alerts()
    assert mw.alert_list_widget.rowCount() == 4


@pytest.mark.test
def test_import_json_db(init_paths, qtbot):
    """Test :class:~_clockalarm.UI.MainWindow.import_json_db method.

    Cannot test the behaviour of this method because it is impossible to access
    the QFileDialog
    """
    pass


@pytest.mark.test
def test_export_json_db(init_paths):
    """Test :class:~_clockalarm.UI.MainWindow.export_json_db method.

    Cannot test the behaviour of this method because it is impossible to access
    the QFileDialog
    """
    pass
