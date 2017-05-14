import configparser
import logging
import pathlib
import shutil
from os.path import join, dirname, abspath

from PyQt5.QtWidgets import qApp, QFileDialog

EXIT_CODE_REBOOT = -11231351

src_path = dirname(dirname(dirname(abspath(__file__))))
config = configparser.RawConfigParser()
config.read(join(src_path, "config.cfg"))


def import_alerts_file():
    src = QFileDialog.getOpenFileName()[0]
    dest = pathlib.Path(join(src_path, 'alertsDB.json')).as_posix()

    if src == '':
        logging.debug("import alerts abort")
        return

    logging.debug("import alerts src path: " + src)
    logging.debug("import alerts dest path: " + dest)

    shutil.copy(src, dest)

    qApp.exit(EXIT_CODE_REBOOT)


def export_alerts_file():
    src = pathlib.Path(join(src_path, 'alertsDB.json')).as_posix()
    dest = QFileDialog.getSaveFileName(None, "Export Alerts List", "alerts.json", filter="json (*.json *.)")[0]

    if dest == "":
        logging.debug("export abort")
        return

    logging.debug("export alerts src path: " + src)
    logging.debug("export alerts dest path: " + dest)

    shutil.copy(src, dest)


def get_default_config(key, cmd="str"):
    if cmd == "int":
        value = config.getint("default", key)
    else:
        value = config.get("default", key)

    logging.debug("default config load(key,value): (" + key + ";" + config.get("default", key) + ")")
    return value
