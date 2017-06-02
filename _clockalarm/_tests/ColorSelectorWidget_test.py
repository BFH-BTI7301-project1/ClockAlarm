import pytest
from PyQt5.QtWidgets import QApplication, QLineEdit, QPushButton

from _clockalarm.UI.ColorSelectorWidget import ColorSelectorWidget

app = QApplication([])


@pytest.mark.test
def test_color_selector_widget_constructor_wrong():
    """Tests the :class:`~_clockalarm.UI.ColorSelectorWidget` constructor.

    Invalid hex_color argument.

    """
    with pytest.raises(ValueError):
        ColorSelectorWidget("#incorrect")


@pytest.mark.test
def test_color_selector_widget_constructor():
    """Tests the :class:`~_clockalarm.UI.SoundSelectorWidget` constructor."""
    cs_widget = ColorSelectorWidget("#111111")

    assert cs_widget.hex_color == "#111111"
    assert isinstance(cs_widget.hex_color_edit, QLineEdit)
    assert cs_widget.hex_color_edit.text() == "#111111"
    assert isinstance(cs_widget.color_select_button, QPushButton)


@pytest.mark.test
def test_color_selector_widget_set_hex_color():
    """Tests the :class:`~_clockalarm.UI.ColorSelectorWidget.set_hex_color` method."""
    cs_widget = ColorSelectorWidget("#111111")
    cs_widget.set_hex_color("#222222")

    assert cs_widget.hex_color == "#222222"
    assert cs_widget.hex_color_edit.text() == "#222222"
