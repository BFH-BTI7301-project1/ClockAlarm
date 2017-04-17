import time

from PyQt5.QtWidgets import QListWidget, QListWidgetItem


class AlertListWidget(QListWidget):
    def __init__(self):
        super(AlertListWidget, self).__init__()
        self.init_ui()

    def init_ui(self):
        if hasattr(self.parent(), 'alert_list'):
            self.actualize(self.parent().alert_list)

    def actualize(self, alert_list):
        self.clear()  # clear the notification box
        for alert in alert_list:
            text = QListWidgetItem()
            text.setText(
                time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(alert.trigger_time)) + " | " + alert.get_identifier())
            self.addItem(text)
            self.setSortingEnabled(True)
