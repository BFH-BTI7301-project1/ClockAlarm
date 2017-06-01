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

import configparser
import logging
import sys
from os.path import dirname, abspath, join, isfile

from PyQt5.Qt import QIcon
from PyQt5.QtCore import QCoreApplication
from PyQt5.QtWidgets import QApplication

from _clockalarm import Clock
from _clockalarm.AlertCollection import AlertCollection
from _clockalarm.NotificationCenter import NotificationCenter
from _clockalarm.UI.MainWindow import MainWindow
from _clockalarm.utils import importExportUtils

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
    def __init__(self, default_config_path, alert_db_path, *argv):
        """Default App constructor
        Override the class constructor
        
        Attributes:
            default_config_path: complete path to the .cfg config file
            alert_db_path: complete path to the .json alert_db file
            *argv: pointer to  the system arguments
            
        """
        super(App, self).__init__(*argv)

        if not isfile(default_config_path) or not default_config_path.lower().endswith('.cfg'):
            raise ValueError("Incorrect configuration file, give a .cfg file")
        if not isfile(alert_db_path) or not alert_db_path.lower().endswith('.json'):
            raise ValueError("Incorrect database file, give a .json file")
        importExportUtils.DEFAULT_CONFIG_PATH = default_config_path
        importExportUtils.ALERT_DB_PATH = alert_db_path

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
        """Open the config_test.cfg file and use a parser to retrieve default values
        
        """
        logging.debug("loading configuration file ...")
        config = configparser.RawConfigParser()  # instantiate a parser to read the stream
        config.read(importExportUtils.DEFAULT_CONFIG_PATH)
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

        self.main_window = MainWindow(self)
        self.main_window.show()
        self.setQuitOnLastWindowClosed(False)  # app don't quit when last window is closed (reduced in tray)

    def init_alert_collection(self):
        """Init AlertCollection object and connect the clock to it
        
        Note:
            The alerts will be loaded from the default database
            
        """
        self.alert_collection = AlertCollection(self)
        self.clock_thread.tick.connect(self.alert_collection.check_timers)


def main(argv):
    """Main function called when application starts

    Attributes:
        argv (optional): path of the config file and the alertDB file
            usage: program configFile alrtDBFile
            If no argument entered, default is config_test.cfg and alertDB.json
        
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

    default_config_path = join(dirname(dirname(abspath(__file__))), "config.cfg")  # default config path
    alert_db_path = join(dirname(dirname(abspath(__file__))), "alertsDB.json")  # default db path
    if len(argv) > 1:  # parse the config path argument
        default_config_path = argv[1]
    if len(argv) > 2:  # parse the db path argument
        alert_db_path = argv[2]
    logging.info("Default configuration file path: " + default_config_path)
    logging.info("Default alertDB path: " + alert_db_path)

    while exit_code == EXIT_CODE_REBOOT:
        # start or reboot
        try:
            app = App(default_config_path, alert_db_path, argv)
            app.init_alert_collection()
        except RuntimeError as e:
            logging.error("RuntimeError : " + e.args[0])
            app = QCoreApplication.instance()
        exit_code = app.exec()  # update exit code

        # properly close the App
        app.clock_thread.stop()
        app.alert_collection.db.close()
        app.main_window.setVisible(False)
        app.main_window.tray_icon.setVisible(False)
        app = None

    return sys.exit(exit_code)


if __name__ == '__main__':
    #  to start from bin
    main(sys.argv)
