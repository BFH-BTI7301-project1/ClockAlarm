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
import shutil
from os.path import dirname, abspath, join, basename

from PyQt5.QtWidgets import QWidget, QPushButton, QLineEdit, QHBoxLayout, QFileDialog, QStyle

src_path = dirname(dirname(dirname(abspath(__file__))))


class SoundSelectorWidget(QWidget):
    def __init__(self, sound_name=None, parent=None):
        super(SoundSelectorWidget, self).__init__(parent)

        self.sound_name = sound_name
        self.sound_edit = None
        self.sound_select_button = None

        self.init_ui()

    def init_ui(self):
        h_layout = QHBoxLayout()

        self.sound_edit = QLineEdit()
        self.sound_select_button = QPushButton()
        self.sound_select_button.setIcon(self.style().standardIcon(QStyle.SP_DirIcon))
        if self.sound_name is not None:
            self.sound_edit.setText(self.sound_name)
        self.sound_select_button.released.connect(self.button_click)

        h_layout.addWidget(self.sound_edit)
        h_layout.addWidget(self.sound_select_button)
        h_layout.setContentsMargins(0, 0, 0, 0)

        self.setLayout(h_layout)

    def button_click(self):
        new_sound = QFileDialog.getOpenFileName(None, "Select a sound to import", filter="wav (*.wav *.)")[0]
        if new_sound == '':
            logging.debug("abort sound import")
            return

        file_name = pathlib.PurePosixPath(new_sound).name
        dest = pathlib.Path(join(src_path, "_clockalarm", "resources", "sounds", file_name)).as_posix()

        logging.debug("import sound src path: " + new_sound)
        logging.debug("import sound dest path: " + dest)

        try:
            shutil.move(new_sound, dest)
        except shutil.Error:
            logging.debug("the sound file already exist")

        self.set_sound(basename(new_sound))

    def set_sound(self, sound):
        self.sound_name = sound
        self.sound_edit.setText(sound)

    def text(self):
        return self.sound_name
