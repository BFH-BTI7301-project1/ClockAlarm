from os.path import dirname, abspath, join

from PyQt5.Qt import QIcon
from PyQt5.QtCore import QSize
from PyQt5.QtWidgets import QMainWindow, QGridLayout, QWidget, QSystemTrayIcon, QMenu, QAction, qApp

from _clockalarm import Notification
from _clockalarm.SimpleAlert import SimpleAlert
from _clockalarm import main
from _clockalarm.UI.AlertListWidget import AlertListWidget
from _clockalarm.UI.SimpleAlertEditWidget import SimpleAlertEditWidget
from _clockalarm.utils.importExportUtils import import_alerts_file, export_alerts_file


class MainWindow(QMainWindow):
    # Override the class constructor
    def __init__(self, *args):
        super(MainWindow, self).__init__(*args)
        self.tray_icon = None
        self.alert_list_widget = None
        self.dialog_widget = None
        self.init_ui()

    def init_ui(self):
        self.setMinimumSize(QSize(300, 100))  # Set sizes
        self.setWindowTitle("ClockAlarm Manager")  # Set a title
        self.resize(800, 400)

        import_action = QAction("Import Alerts File", self)
        import_action.triggered.connect(import_alerts_file)
        export_action = QAction("Export Alerts File", self)
        export_action.triggered.connect(export_alerts_file)
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
        file_menu.addAction(import_action)
        file_menu.addAction(export_action)
        file_menu.addSeparator()
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
        icon_path = join(dirname(dirname(abspath(__file__))), 'resources\\images\\bfh_logo.png')
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
            dw = self.dialog_widget
            new_alert = SimpleAlert(dw.date_time_edit.dateTime().toTime_t(), dw.alert_message_edit.text(),
                                                dw.periodicity_combo.itemData(dw.periodicity_combo.currentIndex()))
            main.app.alert_collection.add(new_alert)
            dw.close()

        self.dialog_widget = SimpleAlertEditWidget()
        self.dialog_widget.accept_button.clicked.connect(button_clicked)

        self.dialog_widget.adjustSize()
        self.dialog_widget.show()

    def edit_simple_alert(self):
        def button_clicked():
            dw = self.dialog_widget
            notification = Notification(dw.alert_message_edit.text())
            trigger_time = dw.date_time_edit.dateTime().toTime_t()
            periodicity = dw.periodicity_combo.itemData(dw.periodicity_combo.currentIndex())
            main.app.alert_collection.edit(notification, trigger_time, id_alert, periodicity)
            dw.close()

        selection = self.alert_list_widget.selectionModel().selectedRows()
        if not selection:
            return

        id_alert = int(self.alert_list_widget.item(selection[0].row(), 0).text())
        alert_to_edit = next(alert for alert in main.app.alert_collection.alert_list if alert.id == id_alert)

        self.dialog_widget = SimpleAlertEditWidget(alert_to_edit)
        self.dialog_widget.accept_button.clicked.connect(button_clicked)

        self.dialog_widget.adjustSize()
        self.dialog_widget.show()

    def delete_alerts(self):
        selection = self.alert_list_widget.selectionModel()
        to_delete = []

        for row in selection.selectedRows():
            to_delete.append(int(self.alert_list_widget.item(row.row(), 0).text()))

        for alert_id in to_delete:
            main.app.alert_collection.delete(alert_id)
