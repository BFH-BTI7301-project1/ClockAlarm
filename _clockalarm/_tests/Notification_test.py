from _clockalarm import Notification
from PyQt5.QtGui import QColor, QFont
from PyQt5.QtMultimedia import QSound

def test_notification():
    notification = Notification("Test")
    
    assert isinstance(notification.color, QColor)
    assert isinstance(notification.font, QFont)
    assert isinstance(notification.sound, QSound)
    assert notification.message == "Test"

