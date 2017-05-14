import time

from PyQt5.QtCore import QDateTime
from PyQt5.QtWidgets import QGridLayout, QWidget, QDateTimeEdit, QLabel, QPushButton, QLineEdit, QGroupBox, QComboBox, \
    QSpinBox

from _clockalarm.SimpleAlert import SimpleAlert
from _clockalarm.UI.ColorSelectorWidget import ColorSelectorWidget
from _clockalarm.UI.SoundSelectorWidget import SoundSelectorWidget


class SimpleAlertEditWidget(QWidget):
    def __init__(self, alert: SimpleAlert = None):
        super(SimpleAlertEditWidget, self).__init__()

        self.alert_message_edit = None
        self.date_time_edit = None
        self.periodicity_combo = None
        self.font_family_edit = None
        self.font_size_edit = None
        self.color_edit = None
        self.sound_edit = None
        self.accept_button = None

        self.init_ui(alert)

    def init_ui(self, alert):
        group_box = QGroupBox(self)
        group_box.setTitle('Set up a new Simple Alert')
        date_time = time.time() + 15
        self.periodicity_combo = QComboBox()
        self.periodicity_combo.addItem("Disable", None)
        self.periodicity_combo.addItem("10 seconds", 10)
        self.periodicity_combo.addItem("1 minute", 60)
        self.date_time_edit = QDateTimeEdit(QDateTime.fromSecsSinceEpoch(date_time))
        self.alert_message_edit = QLineEdit()
        self.font_family_edit = QLineEdit()
        self.font_size_edit = QSpinBox()
        self.font_size_edit.setMaximum(64)
        self.font_size_edit.setSingleStep(2)
        self.color_edit = ColorSelectorWidget()
        self.sound_edit = SoundSelectorWidget()
        self.accept_button = QPushButton('Validate')

        if alert:
            group_box.setTitle('Edit a Simple Alert')
            self.alert_message_edit.setText(alert.get_notification().get_message())
            self.date_time_edit.setDateTime(QDateTime.fromSecsSinceEpoch(alert.trigger_time))
            if alert.notification.font_family is not None:
                self.font_family_edit.setText(alert.notification.font_family)
            if alert.notification.font_size is not None:
                self.font_size_edit.setValue(alert.notification.font_size)
            if alert.notification.color_hex is not None:
                self.color_edit.set_hex_color(alert.notification.color_hex)
            if alert.notification.sound is not None:
                self.sound_edit.set_sound(alert.notification.sound)

        grid_layout = QGridLayout(group_box)
        grid_layout.addWidget(QLabel('Message'), 1, 1)
        grid_layout.addWidget(self.alert_message_edit, 1, 2)
        grid_layout.addWidget(QLabel('Date and Time'), 2, 1)
        grid_layout.addWidget(self.date_time_edit, 2, 2)
        grid_layout.addWidget(QLabel('Periodicity'), 3, 1)
        grid_layout.addWidget(self.periodicity_combo, 3, 2)
        grid_layout.addWidget(QLabel('Font'), 4, 1)
        grid_layout.addWidget(self.font_family_edit, 4, 2)
        grid_layout.addWidget(self.font_size_edit, 4, 3)
        grid_layout.addWidget(QLabel('Text color'), 5, 1)
        grid_layout.addWidget(self.color_edit, 5, 2)
        grid_layout.addWidget(QLabel('Notification sound'), 6, 1)
        grid_layout.addWidget(self.sound_edit, 6, 2)
        grid_layout.addWidget(self.accept_button, 7, 3)

        group_box.setLayout(grid_layout)
        group_box.adjustSize()
