# ClockAlarm is a cross-platform alarm manager
# Copyright (C) 2017  Loïc Charrière, Samuel Gauthier
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

import logging
from os.path import dirname, abspath, join
from shutil import SameFileError

from PyQt5.Qt import QIcon, QTime
from PyQt5.QtCore import QSize, Qt
from PyQt5.QtWidgets import QFileDialog
from PyQt5.QtWidgets import QMainWindow, QGridLayout, QWidget, \
    QSystemTrayIcon, QMenu, QAction, qApp, QPushButton, QStyle

from _clockalarm import Notification
from _clockalarm.SimpleAlert import SimpleAlert
from _clockalarm.UI.AlertListWidget import AlertListWidget
from _clockalarm.UI.SimpleAlertEditWidget import SimpleAlertEditWidget
from _clockalarm.utils.importExportUtils import export_alerts_file, \
    import_alerts_file, set_default_config, get_default_config


class MainWindow(QMainWindow):
    """Main window interface extending :class:`PyQt5.QtWidgets.QMainWindow`.

    Shows a list of all the alerts retrieved from a JSON file.

    Attributes:
        application: The main application
        *args: The parent pointer or window flags
    """

    def __init__(self, application, *args):
        """Creates a main window with an Alert list"""
        super(MainWindow, self).__init__(*args)
        self.app = application
        self.tray_icon = None
        self.alert_list_widget = None
        self.mute_pushbutton = None
        self.dialog_widget = None
        self.init_ui()

    def init_ui(self):
        """Init helper method to set up the main window."""
        self.setMinimumSize(QSize(300, 100))  # Set sizes
        self.setWindowTitle("ClockAlarm Manager")  # Set a title
        self.resize(800, 400)

        import_action = QAction("Import Alerts File", self)
        import_action.triggered.connect(self.import_json_db)
        export_action = QAction("Export Alerts File", self)
        export_action.triggered.connect(self.export_json_db)
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
        self.mute_pushbutton = QPushButton()
        if get_default_config("MUTE", "bool"):
            self.mute_pushbutton.setIcon(self.style().standardIcon(QStyle.SP_MediaVolumeMuted))
        else:
            self.mute_pushbutton.setIcon(self.style().standardIcon(QStyle.SP_MediaVolume))
        self.mute_pushbutton.clicked.connect(self.mute_button_click)

        grid_layout.addWidget(self.alert_list_widget, 0, 0)
        grid_layout.addWidget(self.mute_pushbutton, 1, 0, Qt.AlignRight)

        # Init QSystemTrayIcon
        icon_path = join(dirname(dirname(abspath(__file__))), 'resources', 'images', 'bfh_logo.png')
        icon = QIcon(icon_path)
        self.tray_icon = QSystemTrayIcon(self)
        self.tray_icon.setIcon(icon)
        self.tray_icon.activated.connect(self.tray_icon_click)

        tray_menu = QMenu()
        tray_menu.addAction(quit_action)
        self.tray_icon.setContextMenu(tray_menu)
        self.tray_icon.show()

    def tray_icon_click(self, reason):
        """Displays the main window when clicking on the app icon in the
        tray.
        """
        if reason == QSystemTrayIcon.DoubleClick:
            self.show()

    def mute_button_click(self):
        """Mutes the alerts and updates the mute button."""
        self.app.MUTE = not self.app.MUTE
        if self.app.MUTE:
            self.mute_pushbutton.setIcon(self.style().standardIcon(QStyle.SP_MediaVolumeMuted))
        else:
            self.mute_pushbutton.setIcon(self.style().standardIcon(QStyle.SP_MediaVolume))
        set_default_config("MUTE", self.app.MUTE)

    # Override closeEvent, to intercept the window closing event
    def closeEvent(self, event):
        """Overrides :func:`~PyQt5.QtWidgets.QWidget.closeEvent` method.

        Allows to intercept the window closing event.
        """
        event.ignore()
        self.hide()
        self.tray_icon.showMessage(
            "ClockAlarm",
            "Manager was minimized to Tray",
            QSystemTrayIcon.Information,
            2000
        )

    def add_simple_alert(self):
        """Creates a :class:`~_clockalarm.UI.SimpleAlertEditWidget`
        and shows it to the user.
        """

        def button_clicked():
            dw = self.dialog_widget
            periodicity = QTime(0, 0).secsTo(dw.periodicity_edit.time())
            font_family = dw.font_family_edit.text()
            font_size = dw.font_size_edit.value()
            message = dw.alert_message_edit.text()
            if periodicity == 0:
                periodicity = None
            if font_family == '':
                font_family = None
            if font_size <= 0:
                font_size = None
            if message == '':
                message = "Untitled simple alert"
            notification = Notification(message, font_family=font_family,
                                        font_size=font_size, color_hex=dw.color_edit.hex_color,
                                        sound=dw.sound_edit.sound_name)
            new_alert = SimpleAlert(dw.date_time_edit.dateTime().toTime_t(), notification, periodicity=periodicity)

            self.app.alert_collection.add(new_alert)
            dw.close()

        self.dialog_widget = SimpleAlertEditWidget()
        self.dialog_widget.accept_button.clicked.connect(button_clicked)

        self.dialog_widget.adjustSize()
        self.dialog_widget.show()

    def edit_simple_alert(self):
        """Edits the selected alert and shows an SimpleAlertEditWidget to the
        user.
        """

        def button_clicked():
            dw = self.dialog_widget
            periodicity = QTime(0, 0).secsTo(dw.periodicity_edit.time())
            font_family = dw.font_family_edit.text()
            font_size = dw.font_size_edit.value()
            message = dw.alert_message_edit.text()
            if periodicity == 0:
                periodicity = None
            if font_family == '':
                font_family = None
            if font_size <= 0:
                font_size = None
            if message == '':
                message = "Untitled simple alert"
            notification = Notification(message, font_family=font_family,
                                        font_size=font_size, color_hex=dw.color_edit.hex_color,
                                        sound=dw.sound_edit.sound_name)
            trigger_time = dw.date_time_edit.dateTime().toTime_t()

            try:
                self.app.alert_collection.edit(id_alert, notification=notification, trigger_time=trigger_time,
                                               periodicity=periodicity)
            except KeyError:
                logging.info("The alert to edit doesn't exist anymore")
            dw.close()

        selection = self.alert_list_widget.selectionModel().selectedRows()
        if not selection:
            return

        id_alert = int(self.alert_list_widget.item(selection[0].row(), 0).text())
        alert_to_edit = next(alert for alert in self.app.alert_collection.alert_list if alert.id == id_alert)

        self.dialog_widget = SimpleAlertEditWidget(alert_to_edit)
        self.dialog_widget.accept_button.clicked.connect(button_clicked)

        self.dialog_widget.adjustSize()
        self.dialog_widget.show()

    def delete_alerts(self):
        """Deletes the selected alerts."""
        selection = self.alert_list_widget.selectionModel()
        to_delete = []

        for row in selection.selectedRows():
            to_delete.append(int(self.alert_list_widget.item(row.row(), 0).text()))

        for alert_id in to_delete:
            self.app.alert_collection.delete(alert_id)

    @staticmethod
    def import_json_db():
        """Imports Alerts from a JSON file into ClockAlarm."""
        src = QFileDialog.getOpenFileName(None, 'Import Alert File', '.json', filter='json files (*.json *.JSON *.)')[0]
        if src == '':
            logging.info("import alerts abort")
            return
        try:
            import_alerts_file(src)
        except SameFileError:
            logging.info("the file is already imported")

    @staticmethod
    def export_json_db():
        """Exports all the Alerts into a JSON file."""
        dest = QFileDialog.getSaveFileName(None, "Export Alerts File", "alerts.json",
                                           filter="json files (*.json *.JSON *.)")[0]
        if dest == "":
            logging.info("export abort")
            return
        try:
            export_alerts_file(dest)
        except SameFileError:
            logging.info("the file is already exported")
