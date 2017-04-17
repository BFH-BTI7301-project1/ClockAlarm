import os

from PyQt5.QtGui import QColor, QFont
from PyQt5.QtMultimedia import QSound


class Notification(object):
    def __init__(self, message):
        self.color = QColor(255, 0, 0)
        self.font = QFont("lucida", 12, QFont.Bold, True)
        _sound_path = os.path.join(os.path.dirname(__file__), 'resources\\sounds\\floop.wav')
        self.sound = QSound(_sound_path)
        self.message = message
