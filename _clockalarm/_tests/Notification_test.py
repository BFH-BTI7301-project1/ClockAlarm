from PyQt5.QtGui import QColor, QFont
from pygame import mixer, error
from _clockalarm import Notification


def test_notification():
    """Tests the :class:`~_clockalarm.Notification` constructor."""
    notification = Notification("Test")

    assert notification.message == "Test"
    assert not notification.color_hex
    assert not notification.font_family
    assert not notification.font_size
    assert not notification.sound


def test_get_message():
    """Tests the :class:`~_clockalarm.Notification.get_message` method."""
    notification = Notification("Test")

    assert notification.get_message() == "Test"


def test_get_font():
    """Tests the :class:`~_clockalarm.Notification.get_font` method without any
    font given.
    """
    notification = Notification("Test")

    assert isinstance(notification.get_font(), QFont)


def test_get_color():
    """Tests the :class:`~_clockalarm.Notification.get_color` method without any
    color given.
    """
    notification = Notification("Test")

    assert isinstance(notification.get_color(), QColor)


def test_get_sound():
    """Tests the :class:`~_clockalarm.Notification.get_sound` method without any
    sound given.
    """
    notification = Notification("Test")

    try:
        mixer.init()
        assert isinstance(notification.get_sound(), mixer.Sound)
    except error:
        print("No audio device available!")
