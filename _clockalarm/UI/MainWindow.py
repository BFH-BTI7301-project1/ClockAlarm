import os

from PyQt5.Qt import QIcon
from PyQt5.QtCore import QSize
from PyQt5.QtGui import QImage, QPalette, QBrush
from PyQt5.QtWidgets import QMainWindow, QGridLayout, QWidget, QSystemTrayIcon, QMenu, QAction, qApp, QLabel

from _clockalarm.UI import AlertListWidget


class MainWindow(QMainWindow):
    # Override the class constructor
    def __init__(self, *args):
        super(MainWindow, self).__init__(*args)
        self.tray_icon = None
        self.alert_list_widget = None
        self.init_ui()

    def init_ui(self):
        self.setMinimumSize(QSize(480, 80))  # Set sizes
        self.setWindowTitle("ClockAlarm Manager")  # Set a title
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

        quit_action = QAction("Exit", self)
        quit_action.triggered.connect(qApp.quit)
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
