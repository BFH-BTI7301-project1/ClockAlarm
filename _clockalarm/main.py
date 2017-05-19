import configparser
import logging
import sys
from os.path import dirname, abspath, join

from PyQt5.Qt import QIcon
from PyQt5.QtCore import QCoreApplication
from PyQt5.QtWidgets import QApplication

from _clockalarm import Clock
from _clockalarm.AlertCollection import AlertCollection
from _clockalarm.NotificationCenter import NotificationCenter
from _clockalarm.UI.MainWindow import MainWindow

EXIT_CODE_REBOOT = -11231351  # error code launch by App in case of reboot

app = None  # global
log_format = '%(asctime)s - %(levelname)-8s : %(message)s'
logging.basicConfig(stream=sys.stderr, level=logging.DEBUG, format=log_format)  # set logging level and format


class App(QApplication):
    """Main Application extending QApplication
    
    """
    CLOCK_FREQUENCY = None  # frequency of time checks
    MUTE = None  # general mute of the application

    # Override the class constructor
    def __init__(self, *argv):
        """Default App constructor
        Override the class constructor
        
        Attributes:
            *argv: Pointer on the argument passed to the main
            
        """
        super(App, self).__init__(*argv)
        self.main_window = None
        self.notification_center = None
        self.alert_collection = None
        self.clock_thread = None

        screen_geometry = self.desktop().screenGeometry()  # get the dimensions of the current screen
        logging.info("screen dimensions = (" + str(screen_geometry.width()) + "," + str(screen_geometry.height()) + ")")
        # pass the screen dimensions to the NotificationCenter constructor to init the notification zone
        self.notification_center = NotificationCenter(screen_geometry, parent=self)

        self.init_config()
        self.init_clock(self.CLOCK_FREQUENCY)
        self.init_ui()

    def init_config(self):
        """Open the config.cfg file and use a parser to retrieve default values
        
        """
        logging.debug("loading configuration file ...")
        config_file_path = join(dirname(dirname(abspath(__file__))), "config.cfg")
        config = configparser.RawConfigParser()  # instantiate a parser to read the stream
        config.read(config_file_path)
        self.CLOCK_FREQUENCY = config.getint("default", "CLOCK_FREQUENCY")
        self.MUTE = config.getboolean("default", "MUTE")
        logging.debug("success")

    def init_clock(self, freq):
        """Init and start the Clock with the given frequency
        
        Attributes:
            freq: frequency of the clock's ticks
            
        """
        self.clock_thread = Clock(freq)
        self.clock_thread.start()

    def init_ui(self):
        """Initialisation of the main window GUI
        
        """
        icon_path = join(dirname(abspath(__file__)), 'resources', 'images', 'bfh_logo.png')
        icon = QIcon(icon_path)
        self.setWindowIcon(icon)  # application icon for OSx and linux

        self.main_window = MainWindow()
        self.main_window.show()
        self.setQuitOnLastWindowClosed(False)  # app don't quit when last window is closed (reduced in tray)

    def init_alert_collection(self):
        """Init AlertCollection object and connect the clock to it
        
        Note:
            The alerts will be loaded from the default database
            
        """
        self.alert_collection = AlertCollection(self.notification_center)
        self.clock_thread.tick.connect(self.alert_collection.check_timers)


def main(argv):
    """Main function called when application starts

    Attributes:
        argv: initial program arguments
        
    Returns:
        the system exit code
        
    """
    global app

    exit_code = EXIT_CODE_REBOOT  # exit_code is initially REBOOT

    if sys.platform == "win32":  #
        # workaround to display app icon in task-bar on Windows OS (from http://stackoverflow.com/a/27872625)
        import ctypes
        myappid = u'bfh.project1.clockalarm.1-2'  # arbitrary string (unicode)
        ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)

    while exit_code == EXIT_CODE_REBOOT:
        # start or reboot
        try:
            app = App(sys.argv)
            app.init_alert_collection()
        except RuntimeError as e:
            logging.error("RuntimeError : " + e.args[0])
            app = QCoreApplication.instance()
        exit_code = app.exec()  # update exit code

        # properly close the App
        app.clock_thread.stop()
        app.main_window.setVisible(False)
        app.main_window.tray_icon.setVisible(False)
        app = None

    return sys.exit(exit_code)


if __name__ == '__main__':
    #  to start from bin
    main(sys.argv)
