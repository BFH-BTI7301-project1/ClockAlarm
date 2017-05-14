import logging
import pathlib
from os.path import join, dirname, abspath

from PyQt5.QtGui import QColor, QFont
from pygame import mixer

from _clockalarm.utils.importExportUtils import get_default_config

base_path = dirname(dirname(abspath(__file__)))


class Notification(object):
    def __init__(self, message, color_hex=None, font_family=None, font_size=None, sound=None):
        self.message = message
        self.color_hex = color_hex
        self.font_family = font_family
        self.font_size = font_size
        self.sound = sound

    def get_message(self):
        """Get the message of the Notification

        Returns:
            The text message
        """
        return self.message

    def get_font(self):
        if self.font_family and self.font_size:
            return QFont(self.font_family, self.font_size)
        elif self.font_family:
            return QFont(self.font_family, get_default_config("NOTIFICATION_FONT_SIZE", "int"))
        elif self.font_size:
            return QFont(get_default_config("NOTIFICATION_FONT_FAMILY"), self.font_size)

        return QFont(get_default_config("NOTIFICATION_FONT_FAMILY"),
                     get_default_config("NOTIFICATION_FONT_SIZE", "int"))

    def get_color(self):
        if self.color_hex:
            return QColor(self.color_hex)
        return QColor(get_default_config("NOTIFICATION_COLOR_HEX"))

    def get_sound(self):
        if self.sound:
            _sound_path = pathlib.Path(join(base_path, "_clockalarm", "resources", "sounds", self.sound)).as_posix()
        else:
            _sound_path = pathlib.Path(
                join(base_path, "_clockalarm", "resources", "sounds",
                     get_default_config("NOTIFICATION_SOUND"))).as_posix()

        logging.log(1, "notification sound path: " + _sound_path)
        mixer.init()
        return mixer.Sound(_sound_path)
