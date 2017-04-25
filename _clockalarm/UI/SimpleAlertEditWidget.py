import time

from PyQt5.QtCore import QDateTime
from PyQt5.QtWidgets import QGridLayout, QWidget, QDateTimeEdit, QLabel, QPushButton, QLineEdit, QGroupBox, QComboBox

from _clockalarm import SimpleAlert


class SimpleAlertEditWidget(QWidget):
    def __init__(self, alert: SimpleAlert = None):
        super(SimpleAlertEditWidget, self).__init__()

        self.alert_message_edit = None
        self.date_time_edit = None
        self.periodicity_combo = None
        self.accept_button = None

        self._title = 'Set up a new Simple Alert'
        self._date_time = time.time() + 15
        self._message = ''

        if alert:
            self._title = 'Edit a Simple Alert'
            self._date_time = alert.trigger_time
            self._message = alert.get_identifier()
        self.init_ui()

    def init_ui(self):
        group_box = QGroupBox(self)
        group_box.setTitle(self._title)
        grid_layout = QGridLayout(group_box)
        group_box.setLayout(grid_layout)

        self.alert_message_edit = QLineEdit(self._message)
        self.date_time_edit = QDateTimeEdit(QDateTime.fromSecsSinceEpoch(self._date_time))
        self.periodicity_combo = QComboBox()
        self.periodicity_combo.addItem("Disable", None)
        self.periodicity_combo.addItem("10 seconds", 10)
        self.periodicity_combo.addItem("1 minute", 60)
        self.accept_button = QPushButton('Validate')

        grid_layout.addWidget(QLabel('Message'), 1, 1)
        grid_layout.addWidget(self.alert_message_edit, 1, 2)
        grid_layout.addWidget(QLabel('Date and Time'), 2, 1)
        grid_layout.addWidget(self.date_time_edit, 2, 2)
        grid_layout.addWidget(QLabel('Periodicity'), 3, 1)
        grid_layout.addWidget(self.periodicity_combo, 3, 2)
        grid_layout.addWidget(self.accept_button, 4, 2)

        group_box.adjustSize()
