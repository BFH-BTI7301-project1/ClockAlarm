import sys

from PyQt5.QtWidgets import QApplication

from _clockalarm import Clock
from _clockalarm.AlertCollection import AlertCollection
from _clockalarm.NotificationCenter import NotificationCenter
from _clockalarm.UI import MainWindow

PERIODICITY = 2  # frequency of time checks

app = None


class App(QApplication):
    notification_center = None
    alert_collection = None
    clock_thread = None

    # Override the class constructor
    def __init__(self, *argv):
        super(App, self).__init__(*argv)
        self.clock_thread = None
        self.main_window = None

        screen_geometry = self.desktop().screenGeometry()
        self.notification_center = NotificationCenter(screen_geometry)

        self.init_clock()
        self.init_ui()

    def init_clock(self):
        """CLOCK THREAD"""
        self.clock_thread = Clock(PERIODICITY)
        self.clock_thread.start()

    def init_ui(self):
        self.main_window = MainWindow()
        self.main_window.show()
        self.setQuitOnLastWindowClosed(False)

    def init_alert_collection(self):
        self.alert_collection = AlertCollection(self.notification_center)
        self.clock_thread.tick.connect(self.alert_collection.check_timers)


def main(argv):
    global app

    app = App(sys.argv)
    app.init_alert_collection()
    ret = app.exec()
    app.clock_thread.terminate()  # stops the timer
    app.alert_collection.clean_db()
    sys.exit(ret)


if __name__ == '__main__':
    main(sys.argv)
