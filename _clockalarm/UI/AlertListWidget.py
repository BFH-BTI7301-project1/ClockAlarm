import time

from PyQt5.QtWidgets import QTableWidget, QTableWidgetItem, QAbstractItemView


class AlertListWidget(QTableWidget):
    def __init__(self):
        super(AlertListWidget, self).__init__()
        self.init_ui()

    def init_ui(self):
        self.setColumnCount(3)
        self.setHorizontalHeaderLabels(('ID', 'Time', 'Message'))
        self.verticalHeader().setVisible(False)
        self.horizontalHeader().setStretchLastSection(True)
        self.setSelectionBehavior(QAbstractItemView.SelectRows)

        if hasattr(self.parent(), 'alert_list'):
            self.actualize(self.parent().alert_list)

    def actualize(self, alert_list):
        self.clearContents()  # clear the notification box

        for alert in alert_list:
            self.insertRow(0)
            date = QTableWidgetItem(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(alert.trigger_time)))
            message = QTableWidgetItem(alert.get_identifier())

            self.setItem(0, 0, QTableWidgetItem(str(alert.id)))
            self.setItem(0, 1, date)
            self.setItem(0, 2, message)

        self.resizeColumnToContents(0)
        self.resizeColumnToContents(1)

        self.sortItems(1)
