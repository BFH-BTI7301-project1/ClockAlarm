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


def main(argv):
    global app

    app = App(sys.argv)
    SimpleAlert(time.time() + 3, "This message is delayed: 3 seconds", app.notification_center)
    sys.exit(app.exec())


if __name__ == '__main__':
    main(sys.argv)
