import logging
import pathlib
import shutil
from os.path import dirname, abspath, join

from PyQt5.QtWidgets import qApp, QFileDialog

from _clockalarm import main

src_path = dirname(dirname(dirname(abspath(__file__))))


def import_alerts_file():
    src = QFileDialog.getOpenFileName()[0]
    dest = pathlib.Path(join(src_path, 'alertsDB.json')).as_posix()

    if dest == "":
        logging.debug("import abort")
        return

    logging.debug("import src path: " + src)
    logging.debug("import dest path: " + dest)

    shutil.copy(src, dest)

    qApp.exit(main.EXIT_CODE_REBOOT)


def export_alerts_file():
    src = pathlib.Path(join(src_path, 'alertsDB.json')).as_posix()
    dest = QFileDialog.getSaveFileName(None, "Export Alerts List", "alerts.json", filter="json (*.json *.)")[0]

    if dest == "":
        logging.debug("export abort")
        return

    logging.debug("export src path: " + src)
    logging.debug("export dest path: " + dest)

    shutil.copy(src, dest)
