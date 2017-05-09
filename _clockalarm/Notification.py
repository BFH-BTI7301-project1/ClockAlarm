import configparser
from os.path import join, dirname, abspath

from PyQt5.QtGui import QColor, QFont


class Notification(object):
    def __init__(self, message):
        self.message = message
        self.color = None
        self.font = None
        self.font_size = None
        self.sound = None

        self.load_config()

    def load_config(self):
        base_path = dirname(dirname(abspath(__file__)))

        config = configparser.RawConfigParser()
        config.read(join(base_path, "config.cfg"))

        self.color = QColor(config.get("default", "NOTIFICATION_COLOR"))
        self.font_size = config.getint("default", "NOTIFICATION_FONT_SIZE")
        self.font = QFont(config.get("default", "NOTIFICATION_FONT"), self.font_size, QFont.Bold, True)
        self.sound = config.get("default", "NOTIFICATION_SOUND")


