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

import time

from PyQt5.QtWidgets import QTableWidget, QTableWidgetItem, QAbstractItemView


class AlertListWidget(QTableWidget):
    """Visual list displaying the Alerts from the database."""

    def __init__(self):
        """Default constructor for the :class:`~_clockalarm.UI.AlertListWidget`
        class.
        """
        super(AlertListWidget, self).__init__()
        self.init_ui()

    def init_ui(self):
        """Initialization helper method.

        Creates a visual empty grid with column headers ID, Time, Periodicity
        and Message. If alerts are in the db, fills the list with alerts and
        sorts them.
        """
        self.setColumnCount(4)
        self.setHorizontalHeaderLabels(('ID', 'Time', 'Periodicity',
                                        'Message'))
        self.verticalHeader().setVisible(False)
        self.horizontalHeader().setStretchLastSection(True)
        self.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.setEditTriggers(QAbstractItemView.NoEditTriggers)

    def actualize(self, alert_list):
        """Actualizes the graphical alert list based on the list given in
        argument.

        Attributes:
            alert_list: The list containing all the alerts.
        """
        self.setRowCount(0)  # clear the notification box

        for alert in alert_list:
            self.insertRow(0)
            date = QTableWidgetItem(time.strftime('%Y-%m-%d %H:%M', time.localtime(alert.trigger_time)))
            periodicity = QTableWidgetItem(str(alert.periodicity))
            message = QTableWidgetItem(alert.get_notification().get_message())

            self.setItem(0, 0, QTableWidgetItem(str(alert.id)))
            self.setItem(0, 1, date)
            self.setItem(0, 2, periodicity)
            self.setItem(0, 3, message)

        self.resizeColumnToContents(0)
        self.resizeColumnToContents(1)
        self.resizeColumnToContents(2)

        self.sortItems(1)
