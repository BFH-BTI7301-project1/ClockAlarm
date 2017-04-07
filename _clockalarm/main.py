import sys
import time

from PyQt5.QtWidgets import QApplication

from _clockalarm.NotificationCenter import NotificationCenter
from _clockalarm.SimpleAlert import SimpleAlert
from _clockalarm.UI import MainWindow

app = None


class App(QApplication):
    # Override the class constructor
    def __init__(self, *argv):
        super(App, self).__init__(*argv)
        self.main_window = MainWindow()
        self.main_window.show()
        self.setQuitOnLastWindowClosed(False)
        self.notification_center = NotificationCenter()
        self.alert_list = []


def main(argv):
    global app

    app = App(sys.argv)
    app.alert_list = alerts_from_db()
    app.main_window.alert_list_widget.actualize(app.alert_list)
    sys.exit(app.exec())


if __name__ == '__main__':
    main(sys.argv)


def alerts_from_db():
    global app
    alert_list = []
    alert_5 = SimpleAlert(time.time() + 5, "This message is delayed: 5 seconds", app.notification_center)
    alert_list.append((alert_5._trigger_time, alert_5))
    alert_3 = SimpleAlert(time.time() + 3, "This message is delayed: 3 seconds", app.notification_center)
    alert_list.append((alert_3._trigger_time, alert_3))
    #alert_60 = SimpleAlert(time.time() + 60, "This message is delayed: 60 seconds", app.notification_center)
    #alert_list.append((alert_60._trigger_time, alert_60))
    return alert_list
