import pygame
import pytest
from PyQt5.QtGui import QColor, QFont

from _clockalarm import Notification
from _clockalarm.utils.importExportUtils import get_default_config


def test_notification_constructor():
    """Tests the :class:`~_clockalarm.Notification` constructor."""
    notification = Notification("Test")  # correct constructor
    assert notification.message == "Test"
    assert not notification.color_hex
    assert not notification.font_family
    assert not notification.font_size
    assert not notification.sound

    notification = Notification("Test", "#ffff00", None, None, "test.wav")  # correct constructor
    assert notification.message == "Test"
    assert notification.color_hex == "#ffff00"
    assert not notification.font_family
    assert not notification.font_size
    assert notification.sound == "test.wav"


def test_notification_constructor_exception():
    """Tests the :class:`~_clockalarm.Notification` constructor."""
    with pytest.raises(ValueError):  # message is empty
        Notification("", "#ffff00", None, None, "test.wav")
    with pytest.raises(ValueError):  # message is None
        Notification(None, "#ffff00", None, None, "test.wav")


def test_get_message():
    """Tests the :class:`~_clockalarm.Notification.get_message` method."""
    notification = Notification("Test")

    assert notification.get_message() == "Test"


def test_get_font():
    """Tests the :class:`~_clockalarm.Notification.get_font` method with font given
    """
    notification = Notification("Test", font_family="helvetica", font_size=10)
    font = notification.get_font()
    assert isinstance(font, QFont)
    assert font.family() == "helvetica"
    assert font.pointSize() == 10


def test_get_font_miss_one_arg():
    """Tests the :class:`~_clockalarm.Notification.get_font` method with one parameter missing
    """
    notification = Notification("Test", font_size=10)
    font = notification.get_font()
    assert isinstance(font, QFont)
    assert font.family() == get_default_config("NOTIFICATION_FONT_FAMILY")
    assert font.pointSize() == 10

    notification = Notification("Test", font_family="helvetica")
    font = notification.get_font()
    assert isinstance(font, QFont)
    assert font.family() == "helvetica"
    assert font.pointSize() == get_default_config("NOTIFICATION_FONT_SIZE", "int")


def test_get_font_miss_two_arg():
    """Tests the :class:`~_clockalarm.Notification.get_font` method without any
    font given.
    """
    notification = Notification("Test")
    font = notification.get_font()
    assert isinstance(font, QFont)
    assert font.family() == get_default_config("NOTIFICATION_FONT_FAMILY")
    assert font.pointSize() == get_default_config("NOTIFICATION_FONT_SIZE", "int")


def test_get_color():
    """Tests the :class:`~_clockalarm.Notification.get_color` method.
    """
    notification = Notification("Test", color_hex="#ff5500")
    color = notification.get_color()

    assert isinstance(color, QColor)
    assert color.name() == "#ff5500"


def test_get_color_miss_arg():
    """Tests the :class:`~_clockalarm.Notification.get_color` method without any
    color given.
    """
    notification = Notification("Test")
    color = notification.get_color()

    assert isinstance(color, QColor)
    assert color.name() == get_default_config("NOTIFICATION_COLOR_HEX")


def test_get_sound():
    """Tests the :class:`~_clockalarm.Notification.get_sound` method
    """
    try:
        pygame.mixer.init()

        sound = Notification("Test", sound="floop.wave").get_sound()
        assert isinstance(sound, pygame.mixer.Sound)
    except pygame.error as e:
        print("test_get_sound: {}".format(str(e)))


def test_get_sound_corrupted():
    """Tests the :class:`~_clockalarm.Notification.get_sound` method without any
    sound or corrupted file given.
    """
    try:
        pygame.mixer.init()

        sound = Notification("Test", sound="corrupted.wave").get_sound()
        assert isinstance(sound, pygame.mixer.Sound)
        sound = Notification("Test").get_sound()
        assert isinstance(sound, pygame.mixer.Sound)
    except pygame.error as e:
        print("test_get_sound_corrupted {}".format(str(e)))
