import logging
import os
import pathlib

from PyQt5.QtGui import QColor, QFont
from pygame import mixer


class Notification(object):
    def __init__(self, message):
        self.color = QColor(255, 0, 0)
        self.font = QFont("lucida", 12, QFont.Bold, True)

        _sound_path = pathlib.Path(
            os.path.dirname(os.path.abspath(__file__))).as_posix() + '/resources/sounds/floop.wav'
        logging.log(1, "notification sound path: " + _sound_path)
        mixer.init()
        self.sound = mixer.Sound(_sound_path)

        self.message = message
