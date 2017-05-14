import time

from PyQt5.QtWidgets import QTableWidget, QTableWidgetItem, QAbstractItemView


class AlertListWidget(QTableWidget):
    def __init__(self):
        super(AlertListWidget, self).__init__()
        self.init_ui()

    def init_ui(self):
        self.setColumnCount(4)
        self.setHorizontalHeaderLabels(('ID', 'Time', 'Periodicity', 'Message'))
        self.verticalHeader().setVisible(False)
        self.horizontalHeader().setStretchLastSection(True)
        self.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.setEditTriggers(QAbstractItemView.NoEditTriggers)

        if hasattr(self.parent(), 'alert_list'):
            self.actualize(self.parent().alert_list)

    def actualize(self, alert_list):
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
