import sys

from PyQt5.QtCore import QCoreApplication
from PyQt5.QtWidgets import QApplication

from _clockalarm import Clock
from _clockalarm.AlertCollection import AlertCollection
from _clockalarm.NotificationCenter import NotificationCenter
from _clockalarm.UI import MainWindow

PERIODICITY = 2  # frequency of time checks
EXIT_CODE_REBOOT = -11231351

app = None


class App(QApplication):
    # Override the class constructor
    def __init__(self, *argv):
        super(App, self).__init__(*argv)
        self.main_window = None
        self.notification_center = None
        self.alert_collection = None
        self.clock_thread = None

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

    exit_code = EXIT_CODE_REBOOT

    while exit_code == EXIT_CODE_REBOOT:
        try:
            app = App(sys.argv)
            app.init_alert_collection()
        except RuntimeError:
            app = QCoreApplication.instance()
        exit_code = app.exec()
        app.clock_thread.stop()
        app = None
    sys.exit(exit_code)


if __name__ == '__main__':
    main(sys.argv)
