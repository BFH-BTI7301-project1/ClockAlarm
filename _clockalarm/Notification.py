import configparser
import logging
import pathlib
from os.path import join, dirname, abspath

from PyQt5.QtGui import QColor, QFont
from pygame import mixer


class Notification(object):
    def __init__(self, message):
        self.message = message
        self.color = None
        self.font = None
        self.sound = None

        self.load_config()

    def load_config(self):
        base_path = dirname(dirname(abspath(__file__)))

        config = configparser.RawConfigParser()
        config.read(join(base_path, "config.cfg"))

        self.color = QColor(config.get("default", "NOTIFICATION_COLOR"))
        self.font = QFont(config.get("default", "NOTIFICATION_FONT"),
                          config.getint("default", "NOTIFICATION_FONT_SIZE"), QFont.Bold, True)

        _sound_path = pathlib.Path(join(base_path, "_clockalarm", "resources", "sounds",
                                        config.get("default", "NOTIFICATION_SOUND"))).as_posix()
        logging.log(1, "notification sound path: " + _sound_path)
        mixer.init()
        self.sound = mixer.Sound(_sound_path)
