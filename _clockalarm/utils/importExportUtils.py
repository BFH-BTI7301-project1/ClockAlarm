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
import pathlib
import shutil
from os.path import join, dirname, abspath

from PyQt5.QtWidgets import qApp, QFileDialog

EXIT_CODE_REBOOT = -11231351

src_path = dirname(dirname(dirname(abspath(__file__))))
alert_file_path = join(src_path, "alertsDB.json")
config_file_path = join(src_path, "config.cfg")


def import_alerts_file():
    src = QFileDialog.getOpenFileName()[0]
    dest = pathlib.Path(alert_file_path).as_posix()

    if src == '':
        logging.debug("import alerts abort")
        return

    logging.debug("import alerts src path: " + src)
    logging.debug("import alerts dest path: " + dest)

    shutil.copy(src, dest)

    qApp.exit(EXIT_CODE_REBOOT)


def export_alerts_file():
    src = pathlib.Path(alert_file_path).as_posix()
    dest = QFileDialog.getSaveFileName(None, "Export Alerts List", "alerts.json", filter="json (*.json *.)")[0]

    if dest == "":
        logging.debug("export abort")
        return

    logging.debug("export alerts src path: " + src)
    logging.debug("export alerts dest path: " + dest)

    shutil.copy(src, dest)


def get_default_config(key, cmd="str"):
    config = configparser.RawConfigParser()
    config.read(config_file_path)
    if cmd == "int":
        value = config.getint("default", key)
    elif cmd == "bool":
        value = config.getboolean("default", key)
    else:
        value = config.get("default", key)

    logging.debug("default config load(key,value): (" + key + ";" + str(value) + ")")
    return value


def set_default_config(key, value):
    config = configparser.RawConfigParser()
    config.optionxform = str
    config.read(config_file_path)
    config.set("default", key, str(value))
    with open(config_file_path, 'w') as configfile:
        config.write(configfile)

    logging.debug("default config set(key,value): (" + key + ";" + str(value) + ")")
