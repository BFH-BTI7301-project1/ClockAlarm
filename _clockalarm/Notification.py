# ClockAlarm is a cross-platform alarm manager
# Copyright (C) 2017  Loïc Charrière, Samuel Gauthier
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

import logging
import pathlib
from os.path import join, dirname, abspath, isfile

from PyQt5.QtGui import QColor, QFont
from pygame import mixer

from _clockalarm.utils.importExportUtils import get_default_config

base_path = dirname(dirname(abspath(__file__)))


class Notification(object):
    """Encapsulate the parameters of a Notification in order to pass it to the NotificationCenter
    
    """

    def __init__(self, message: str, color_hex: str = None, font_family: str = None,
                 font_size: int = None, sound: str = None):
        """Default Notification constructor
        
        Args:
            message (str): text of the notification.
            color_hex (str, optional): default to None. Color of the text in hexadecimal. 
            font_family (str, optional): default to None. Font of the notification
            font_size (int, optional): default to None. Size of the font for the notification
            sound (str, optional): default to None. Path of the sound played when the notification occur
        
        Raises:
            ValueError: if the message is empty
            
        """
        if message is None or message == '':
            raise ValueError("The notification message can't be empty")

        self.message = message
        self.color_hex = color_hex
        self.font_family = font_family
        self.font_size = font_size
        self.sound = sound

    def get_message(self):
        """Getter for message

        Returns:
            The notification text
            
        """
        return self.message

    def get_font(self):
        """Build a QFont from font_family and font_size
        
        If font_family or font_size parameter is missing, replace it with de default configuration.
        
        Returns:
            The QFont of the notification
            
        """
        if self.font_family and self.font_size:  # both parameters available
            return QFont(self.font_family, self.font_size)
        elif self.font_family:  # missing font_size
            return QFont(self.font_family, get_default_config(
                "NOTIFICATION_FONT_SIZE", "int"))
        elif self.font_size:  # missing font_family
            return QFont(get_default_config("NOTIFICATION_FONT_FAMILY"),
                         self.font_size)

        return QFont(get_default_config("NOTIFICATION_FONT_FAMILY"),
                     get_default_config("NOTIFICATION_FONT_SIZE", "int"))  # missing both parameters

    def get_color(self):
        """Build a QColor from color_hex parameter

        If color_hex parameter is missing, replace it with de default configuration.

        Returns:
            The QColor of the notification
            
        """
        if self.color_hex:
            return QColor(self.color_hex)
        return QColor(get_default_config("NOTIFICATION_COLOR_HEX"))  # missing color_hex parameter

    def get_sound(self):
        """Build a mixer.Sound object from sound parameter

        If the sound path parameter is missing, replace it with de default configuration.

        Returns:
            The mixer.Sound file of the notification

        """
        _sound_path = None
        if self.sound:  # existing sound path in Notification parameters
            _sound_path = pathlib.Path(join(base_path, "_clockalarm",
                                            "resources", "sounds",
                                            self.sound)).as_posix()
        if _sound_path is None or not isfile(_sound_path):  # incorrect or missing sound path
            _sound_path = pathlib.Path(
                join(base_path, "_clockalarm", "resources", "sounds",
                     get_default_config("NOTIFICATION_SOUND"))).as_posix()  # replace with default sound path

        logging.log(1, "notification sound path: " + _sound_path)

        mixer.init()
        return mixer.Sound(_sound_path)  # returns the sound in a mixer.Sound object
