import logging
import re

from PyQt5.QtGui import QColor
from PyQt5.QtWidgets import QWidget, QPushButton, QLineEdit, QColorDialog, QHBoxLayout


class ColorSelectorWidget(QWidget):
    def __init__(self, hex_color=None, parent=None):
        super(ColorSelectorWidget, self).__init__(parent)

        self.hex_color = hex_color
        self.hex_color_edit = None
        self.color_select_button = None

        self.init_ui()

    def init_ui(self):
        h_layout = QHBoxLayout()

        self.hex_color_edit = QLineEdit()
        self.color_select_button = QPushButton()
        if self.hex_color is not None:
            self.set_hex_color(self.hex_color)
        self.hex_color_edit.textChanged.connect(self.change_event)
        self.color_select_button.released.connect(self.button_click)

        h_layout.addWidget(self.hex_color_edit)
        h_layout.addWidget(self.color_select_button)
        h_layout.setContentsMargins(0, 0, 0, 0)

        self.setLayout(h_layout)

    def button_click(self):
        if self.hex_color:
            new_color = QColorDialog.getColor(QColor(self.hex_color))
        else:
            new_color = QColorDialog.getColor()

        if not new_color.isValid():
            logging.debug("abort color selection")
            return
        self.set_hex_color(new_color.name())

    def set_hex_color(self, hex_color):
        self.hex_color = hex_color
        self.hex_color_edit.setText(hex_color)
        self.color_select_button.setStyleSheet("QPushButton { background-color : " + hex_color + "}")

    def change_event(self):
        current_hex = self.hex_color_edit.text()
        if re.search(r'^#(?:[0-9a-fA-F]{3}){1,2}$', current_hex):
            self.hex_color = current_hex
            self.color_select_button.setStyleSheet("QPushButton { background-color : " + current_hex + "}")

    def text(self):
        return self.hex_color
