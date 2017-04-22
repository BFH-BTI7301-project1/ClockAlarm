from PyQt5.QtGui import QColor, QFont
from PyQt5.QtMultimedia import QSound

from _clockalarm import Notification


def test_notification():
    """Tests the :class:`~_clockalarm.Notification` constructor."""
    notification = Notification("Test")

    assert isinstance(notification.color, QColor)
    assert isinstance(notification.font, QFont)
    assert isinstance(notification.sound, QSound)
    assert notification.message == "Test"

