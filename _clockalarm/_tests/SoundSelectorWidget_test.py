import filecmp
import os
from os.path import dirname, join, abspath

import pytest
from PyQt5.QtWidgets import QApplication, QLineEdit, QPushButton

from _clockalarm.UI.SoundSelectorWidget import SoundSelectorWidget

app = QApplication([])


@pytest.mark.test
def test_sound_selector_widget_constructor_wrong():
    """Tests the :class:`~_clockalarm.UI.SoundSelectorWidget` constructor.

    Invalid sound_name argument.

    """
    with pytest.raises(ValueError):
        SoundSelectorWidget("mySound.mp3")


@pytest.mark.test
def test_sound_selector_widget_constructor():
    """Tests the :class:`~_clockalarm.UI.SoundSelectorWidget` constructor."""
    ss_widget = SoundSelectorWidget("mySound.wav")

    assert ss_widget.sound_name == "mySound.wav"
    assert isinstance(ss_widget.sound_edit, QLineEdit)
    assert ss_widget.sound_edit.text() == "mySound.wav"
    assert isinstance(ss_widget.sound_select_button, QPushButton)


@pytest.mark.test
def test_sound_selector_widget_set_sound_wrong():
    """Tests the :class:`~_clockalarm.UI.SoundSelectorWidget.set_sound` method.

    Incorrect sound argument.

    """
    ss_widget = SoundSelectorWidget("mySound.wav")
    with pytest.raises(ValueError):
        ss_widget.set_sound("wrong_ext.mp3")


@pytest.mark.test
def test_sound_selector_widget_set_sound():
    """Tests the :class:`~_clockalarm.UI.SoundSelectorWidget.set_sound` method."""
    ss_widget = SoundSelectorWidget("mySound.wav")
    ss_widget.set_sound("new_sound.wav")

    assert ss_widget.sound_name == "new_sound.wav"
    assert ss_widget.sound_edit.text() == "new_sound.wav"


@pytest.mark.test
def test_sound_selector_widget_load_sound_error():
    """Tests the :class:`~_clockalarm.UI.SoundSelectorWidget.load_sound` method.

    Corrupted sound_path argument

    """
    ss_widget = SoundSelectorWidget("mySound.wav")
    with pytest.raises(ValueError):
        ss_widget.load_sound(None)
    with pytest.raises(ValueError):
        ss_widget.load_sound("incorrect.mp3")


@pytest.mark.test
def test_sound_selector_widget_load_sound():
    """Tests the :class:`~_clockalarm.UI.SoundSelectorWidget.load_sound` method."""
    import pathlib
    ss_widget = SoundSelectorWidget("mySound.wav")

    src_sound_file = join(dirname(abspath(__file__)), "test_sound.wav")
    dest_sound_path = join(dirname(dirname(abspath(__file__))), "resources", "sounds")
    ss_widget.load_sound(pathlib.Path(src_sound_file).as_posix())

    assert filecmp.cmp(src_sound_file, join(dest_sound_path, "test_sound.wav"))
    assert ss_widget.sound_name == "test_sound.wav"

    os.remove(join(dest_sound_path, "test_sound.wav"))
