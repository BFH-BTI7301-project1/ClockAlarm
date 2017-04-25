import os

from PyQt5.Qt import QIcon
from PyQt5.QtCore import QSize
from PyQt5.QtWidgets import QMainWindow, QGridLayout, QWidget, QSystemTrayIcon, QMenu, QAction, qApp

from _clockalarm import SimpleAlert, Notification
from _clockalarm import main
from _clockalarm.UI import AlertListWidget, SimpleAlertEditWidget


class MainWindow(QMainWindow):
    # Override the class constructor
    def __init__(self, *args):
        super(MainWindow, self).__init__(*args)
        self.tray_icon = None
        self.alert_list_widget = None
        self.dialog_widget = None
        self.init_ui()

    def init_ui(self):
        self.setMinimumSize(QSize(400, 120))  # Set sizes
        self.setWindowTitle("ClockAlarm Manager")  # Set a title

        quit_action = QAction("Exit", self)
        quit_action.triggered.connect(qApp.quit)

        new_alert_action = QAction("New Simple Alert", self)
        new_alert_action.triggered.connect(self.add_simple_alert)
        delete_alert_action = QAction("Delete Alert", self)
        delete_alert_action.triggered.connect(self.delete_alerts)
        edit_alert_action = QAction("Edit Alert", self)
        edit_alert_action.triggered.connect(self.edit_simple_alert)

        menu_bar = self.menuBar()
        file_menu = menu_bar.addMenu('&File')
        edit_menu = menu_bar.addMenu('&Edit')
        file_menu.addAction(quit_action)
        edit_menu.addAction(new_alert_action)
        edit_menu.addAction(delete_alert_action)
        edit_menu.addAction(edit_alert_action)

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

    def add_simple_alert(self):
        def button_clicked():
            new_alert = SimpleAlert(self.dialog_widget.date_time_edit.dateTime().toTime_t(),
                                    self.dialog_widget.alert_message_edit.text())
            main.app.alert_collection.add(new_alert)
            self.dialog_widget.close()

        self.dialog_widget = SimpleAlertEditWidget.SimpleAlertEditWidget()
        self.dialog_widget.accept_button.clicked.connect(button_clicked)

        self.dialog_widget.adjustSize()
        self.dialog_widget.show()

    def edit_simple_alert(self):
        def button_clicked():
            notification = Notification(self.dialog_widget.alert_message_edit.text())
            trigger_time = self.dialog_widget.date_time_edit.dateTime().toTime_t()
            main.app.alert_collection.edit(notification, trigger_time, id_alert)
            self.dialog_widget.close()

        selection = self.alert_list_widget.selectionModel().selectedRows()
        if not selection:
            return

        id_alert = int(self.alert_list_widget.item(selection[0].row(), 0).text())
        alert_to_edit = next(alert for alert in main.app.alert_collection.alert_list if alert.id == id_alert)

        self.dialog_widget = SimpleAlertEditWidget.SimpleAlertEditWidget(alert_to_edit)
        self.dialog_widget.accept_button.clicked.connect(button_clicked)
        self.dialog_widget.adjustSize()
        self.dialog_widget.show()

    def delete_alerts(self):
        selection = self.alert_list_widget.selectionModel()

        for row in selection.selectedRows():
            alert_id = int(self.alert_list_widget.item(row.row(), 0).text())
            main.app.alert_collection.delete(alert_id)
