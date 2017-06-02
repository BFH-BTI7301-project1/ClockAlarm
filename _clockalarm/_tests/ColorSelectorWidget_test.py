import pytest
from PyQt5.QtWidgets import QApplication, QLineEdit, QPushButton

from _clockalarm.UI.ColorSelectorWidget import ColorSelectorWidget

app = QApplication([])


@pytest.mark.skip
def test_color_selector_widget_constructor_wrong():
    """Tests the :class:`~_clockalarm.UI.ColorSelectorWidget` constructor.

    Invalid sound_name argument.

    """
    with pytest.raises(ValueError):
        SoundSelectorWidget("mySound.mp3")


@pytest.mark.skip
def test_sound_selector_widget_constructor():
    """Tests the :class:`~_clockalarm.UI.SoundSelectorWidget` constructor."""
    ss_widget = SoundSelectorWidget("mySound.wav")

    assert ss_widget.sound_name == "mySound.wav"
    assert isinstance(ss_widget.sound_edit, QLineEdit)
    assert ss_widget.sound_edit.text() == "mySound.wav"
    assert isinstance(ss_widget.sound_select_button, QPushButton)


@pytest.mark.skip
def test_sound_selector_widget_set_sound_wrong():
    """Tests the :class:`~_clockalarm.UI.SoundSelectorWidget.set_sound` method.

    Incorrect sound argument.

    """
    ss_widget = SoundSelectorWidget("mySound.wav")
    with pytest.raises(ValueError):
        ss_widget.set_sound("wrong_ext.mp3")


@pytest.mark.skip
def test_sound_selector_widget_set_sound():
    """Tests the :class:`~_clockalarm.UI.SoundSelectorWidget.set_sound` method."""
    ss_widget = SoundSelectorWidget("mySound.wav")
    ss_widget.set_sound("new_sound.wav")

    assert ss_widget.sound_name == "new_sound.wav"
    assert ss_widget.sound_edit.text() == "new_sound.wav"
