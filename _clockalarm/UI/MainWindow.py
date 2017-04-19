import os

from PyQt5.Qt import QIcon
from PyQt5.QtCore import QSize, QDateTime
from PyQt5.QtWidgets import QMainWindow, QGridLayout, QWidget, QSystemTrayIcon, QMenu, QAction, qApp, QDateTimeEdit, \
    QLineEdit, QLabel, QGroupBox, QPushButton

from _clockalarm import SimpleAlert
from _clockalarm import main
from _clockalarm.UI import AlertListWidget


class MainWindow(QMainWindow):
    # Override the class constructor
    def __init__(self, *args):
        super(MainWindow, self).__init__(*args)
        self.tray_icon = None
        self.alert_list_widget = None
        self.dialog_widget = None
        self.init_ui()

    def init_ui(self):
        self.setMinimumSize(QSize(480, 80))  # Set sizes
        self.setWindowTitle("ClockAlarm Manager")  # Set a title

        quit_action = QAction("Exit", self)
        quit_action.triggered.connect(qApp.quit)

        new_alert_action = QAction("New Simple Alert", self)
        new_alert_action.triggered.connect(self.add_simple_alert_dialogue)

        menu_bar = self.menuBar()
        file_menu = menu_bar.addMenu('&File')
        edit_menu = menu_bar.addMenu('&Edit')
        file_menu.addAction(quit_action)
        edit_menu.addAction(new_alert_action)

        central_widget = QWidget(self)  # Create a central widget
        self.setCentralWidget(central_widget)  # Set the central widget

        grid_layout = QGridLayout(central_widget)  # Create a QGridLayout
        central_widget.setLayout(grid_layout)  # Set the layout into the central widget
        self.alert_list_widget = AlertListWidget()
        grid_layout.addWidget(self.alert_list_widget)

        # Init QSystemTrayIcon
        icon_path = os.path.join(os.path.dirname(__file__), '..\\resources\\images\\bfh_logo.png')
        icon = QIcon(icon_path)
        self.tray_icon = QSystemTrayIcon(self)
        self.tray_icon.setIcon(icon)
        self.tray_icon.activated.connect(self.tray_icon_click)

        tray_menu = QMenu()
        tray_menu.addAction(quit_action)
        self.tray_icon.setContextMenu(tray_menu)
        self.tray_icon.show()

    def tray_icon_click(self, reason):
        if reason == QSystemTrayIcon.DoubleClick:
            self.show()

    # Override closeEvent, to intercept the window closing event
    def closeEvent(self, event):
        event.ignore()
        self.hide()
        self.tray_icon.showMessage(
            "ClockAlarm",
            "Manager was minimized to Tray",
            QSystemTrayIcon.Information,
            2000
        )

    def add_simple_alert_dialogue(self):
        self.dialog_widget = QWidget()
        group_box = QGroupBox(self.dialog_widget)
        group_box.setTitle('Set up a new Simple Alert')
        grid_layout = QGridLayout(group_box)
        group_box.setLayout(grid_layout)

        self.alert_message_edit = QLineEdit()
        self.date_time_edit = QDateTimeEdit(QDateTime.currentDateTime().addSecs(15))
        accept_button = QPushButton('Validate')

        accept_button.clicked.connect(self.button_clicked)

        grid_layout.addWidget(QLabel('Message'), 1, 1)
        grid_layout.addWidget(self.alert_message_edit, 1, 2)
        grid_layout.addWidget(QLabel('Date and Time'), 2, 1)
        grid_layout.addWidget(self.date_time_edit, 2, 2)
        grid_layout.addWidget(accept_button, 3, 2)

        group_box.adjustSize()
        self.dialog_widget.adjustSize()
        self.dialog_widget.show()

    def button_clicked(self):
        main.app.alert_collection.add(
            SimpleAlert(self.date_time_edit.dateTime().toTime_t(), self.alert_message_edit.text()))
        self.dialog_widget.close()
