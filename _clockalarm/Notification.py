import logging
import os
import pathlib

from PyQt5 import QtMultimedia
from PyQt5.QtCore import QUrl
from PyQt5.QtGui import QColor, QFont


class Notification(object):
    def __init__(self, message):
        self.color = QColor(255, 0, 0)
        self.font = QFont("lucida", 12, QFont.Bold, True)

        _sound_path = pathlib.Path(
            os.path.dirname(os.path.abspath(__file__))).as_posix() + '/resources/sounds/floop.mp3'
        logging.debug("notification sound path: " + _sound_path)
        self.sound = QtMultimedia.QMediaContent(QUrl(_sound_path))

        self.message = message
