from os.path import join, abspath, dirname

import pytest
from PyQt5 import QtCore
from PyQt5.Qt import QRect
from PyQt5.QtCore import Qt, QPoint
from PyQt5.QtWidgets import QApplication, QLabel

from _clockalarm.Notification import Notification
from _clockalarm.UI.NotificationWidget import NotificationWidget
from _clockalarm.utils import importExportUtils


@pytest.fixture
def init_paths(scope="module"):
    importExportUtils.DEFAULT_CONFIG_PATH = join(dirname(abspath(__file__)),
                                                 "config_test.cfg")
    importExportUtils.ALERT_DB_PATH = join(dirname(abspath(__file__)),
                                           "alertsDB_test.json")


sound_path = join(dirname(dirname(abspath(__file__))), 'resources', 'sounds',
                  'floop.wav')
im_path = join(dirname(dirname(abspath(__file__))), 'resources', 'images',
               'notification_clock.png')

notification = Notification("Test", "000000", "Times", 12, sound_path)
rect = QRect(0, 0, 1024, 768)

# A QApplication is needed to create widgets
app = QApplication([])


def test_constructor(init_paths):
    """Test :class:~_clockalarm.UI.NotificationWidget constructor."""
    global notification
    global rect

    nw = NotificationWidget(rect, notification)

    assert nw.notification.message == "Test"
    assert nw.height() == rect.height()
    assert nw.width() == rect.width()
    assert nw.x() == rect.x()
    assert nw.y() == rect.y()
    assert nw.windowOpacity() == 0.8
    assert nw.autoFillBackground()
    assert nw.testAttribute(Qt.WA_ShowWithoutActivating)

    children = nw.findChildren(QLabel)

    # Background image
    assert not children[0].pixmap().isNull()

    # Notification message
    assert children[1].alignment() == Qt.AlignTop
    assert children[1].wordWrap()
    assert children[1].font().family() == notification.font_family


def test_mousePressedEvent(qtbot, init_paths):
    """Test :class:~_clockalarm.UI.NotificationWidget.mousPressEvent method."""
    global notification
    global rect

    nw = NotificationWidget(rect, notification)

    qtbot.addWidget(nw)

    with qtbot.waitExposed(nw):
        nw.show()

    with qtbot.waitSignal(nw.popup_close, raising=True):
        qtbot.mouseMove(nw, QPoint(0, 0))
        qtbot.mouseClick(nw, QtCore.Qt.LeftButton)
