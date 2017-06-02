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
import re

from PyQt5.QtGui import QColor
from PyQt5.QtWidgets import QWidget, QPushButton, QLineEdit, QColorDialog, QHBoxLayout


class ColorSelectorWidget(QWidget):
    """Costumed widget to selected a color for the notification"""

    def __init__(self, hex_color=None, parent=None):
        """ColorSelectorWidget default constructor

        Attributes:
            hex_color (str, optional): Initialization hexadecimal color value
            parent (QWidget, optional): Parent QWidget

        """
        super(ColorSelectorWidget, self).__init__(parent)

        if hex_color and not re.search(r'^#(?:[0-9a-fA-F]{3}){1,2}$', hex_color):
            raise ValueError(hex_color + ' is not a correct hexadecimal value')

        self.hex_color = hex_color
        self.hex_color_edit = None
        self.color_select_button = None

        self.init_ui()

    def init_ui(self):
        """Initialize the GUI of the QWidget

        """
        h_layout = QHBoxLayout()

        self.hex_color_edit = QLineEdit()
        self.color_select_button = QPushButton()
        if self.hex_color is not None:  # init the text in QLineEdit
            self.set_hex_color(self.hex_color)
        self.hex_color_edit.textChanged.connect(self.change_event)  # event to change the button color
        self.color_select_button.released.connect(self.button_click)

        h_layout.addWidget(self.hex_color_edit)
        h_layout.addWidget(self.color_select_button)
        h_layout.setContentsMargins(0, 0, 0, 0)

        self.setLayout(h_layout)

    def button_click(self):
        """Called when the color_select_button is clicked.

        Choose a color from a palette.

        """
        if self.hex_color:
            new_color = QColorDialog.getColor(QColor(self.hex_color))  # init with color
        else:
            new_color = QColorDialog.getColor()

        if not new_color.isValid():
            logging.debug("abort color selection")
            return
        self.set_hex_color(new_color.name())

    def set_hex_color(self, hex_color):
        """Set a new hexadecimal color

        Attributes:
            hex_color (str): The new color.

        """

        self.hex_color = hex_color
        self.hex_color_edit.setText(hex_color)
        self.color_select_button.setStyleSheet("QPushButton { background-color : " + hex_color + "}")

    def change_event(self):
        """Called every times the QLineEdit field is updated.

        Update the hex_color value and the color of the QPushButton.

        """
        current_hex = self.hex_color_edit.text()
        if re.search(r'^#(?:[0-9a-fA-F]{3}){1,2}$',
                     current_hex):  # only update the color if it's a correct hexadecimal string
            self.hex_color = current_hex
            self.color_select_button.setStyleSheet("QPushButton { background-color : " + current_hex + "}")
