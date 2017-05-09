import configparser
import logging
import sys
from os.path import dirname, abspath, join

from PyQt5.QtCore import QCoreApplication
from PyQt5.QtWidgets import QApplication

from _clockalarm import Clock
from _clockalarm.AlertCollection import AlertCollection
from _clockalarm.NotificationCenter import NotificationCenter
from _clockalarm.UI.MainWindow import MainWindow

EXIT_CODE_REBOOT = -11231351

app = None
logging.basicConfig(stream=sys.stderr, level=logging.DEBUG)


class App(QApplication):
    CLOCK_FREQUENCY = None  # frequency of time checks
    MUTE = None

    # Override the class constructor
    def __init__(self, *argv):
        super(App, self).__init__(*argv)
        self.main_window = None
        self.notification_center = None
        self.alert_collection = None
        self.clock_thread = None

        screen_geometry = self.desktop().screenGeometry()
        self.notification_center = NotificationCenter(screen_geometry, parent=self)

        self.init_config()
        self.init_clock()
        self.init_ui()

    def init_clock(self):
        """CLOCK THREAD"""
        self.clock_thread = Clock(self.CLOCK_FREQUENCY)
        self.clock_thread.start()

    def init_ui(self):
        self.main_window = MainWindow()
        self.main_window.show()
        self.setQuitOnLastWindowClosed(False)

    def init_config(self):
        logging.debug("loading configuration file ...")

        config_file_path = join(dirname(dirname(abspath(__file__))), "config.cfg")
        config = configparser.RawConfigParser()
        config.read(config_file_path)
        self.CLOCK_FREQUENCY = config.getint("default", "CLOCK_FREQUENCY")
        self.MUTE = config.getboolean("default", "MUTE")
        logging.debug("success")

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
        except RuntimeError as e:
            logging.error(e.strerror)
            app = QCoreApplication.instance()
        exit_code = app.exec()
        app.clock_thread.stop()
        app.main_window.tray_icon.setVisible(False)
        app = None
    sys.exit(exit_code)


if __name__ == '__main__':
    main(sys.argv)
