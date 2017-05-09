import logging
import pathlib
import shutil
from os.path import dirname, abspath, join

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

        self.setLayout(h_layout)

    @staticmethod
    def button_click():
        new_sound = QFileDialog.getOpenFileName(None, "Select a sound to import", filter="wav (*.wav *.)")[0]
        if new_sound == '':
            logging.debug("abort sound import")
            return

        file_name = pathlib.PurePosixPath(new_sound).name
        dest = pathlib.Path(join(src_path, "_clockalarm", "resources", "sounds", file_name)).as_posix()

        logging.debug("import sound src path: " + new_sound)
        logging.debug("import sound dest path: " + dest)

        shutil.copy(new_sound, dest)

    def set_sound(self, sound):
        self.sound_name = sound
        self.sound_edit.setText(sound)
