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
from os.path import isfile

from PyQt5.QtWidgets import qApp

EXIT_CODE_REBOOT = -11231351  # exit code to reboot the app

DEFAULT_CONFIG_PATH = ""
ALERT_DB_PATH = ""


def import_alerts_file(src):
    """Copy the .json file given as argument into the location specified by ALERT_DB_PATH

    If existing, the destination file is erased.
    All the application is restarted after an import.

    Arguments:
        src (str): full path of the source json database

    Exceptions:
        FileNotFoundException: If the given source file doesn't exist or isn't a json file
        SameFileError: If the src and destination files are the same

    """
    if src is None or not src.endswith(('.json', '.JSON)')) or not isfile(src):
        raise FileNotFoundError("Source isn't a correct JSON file")

    dest = pathlib.Path(ALERT_DB_PATH).as_posix()

    logging.debug("import alerts src path: " + src)
    logging.debug("import alerts dest path: " + dest)
    shutil.copy(src, dest)  # raises SameFileError

    qApp.exit(EXIT_CODE_REBOOT)


def export_alerts_file(dest):
    """Copy the file at ALERT_DB_PATH into the .json location specified the argument

    If existing, the destination file is erased.

    Arguments:
        dest (str): full path of the destination location

    Exceptions:
        FileNotFoundException: If the given destination file doesn't exist or haven't a json extension
        shutil.SameFileError: If the src and destination files are the same

    """
    if dest is None or not dest.endswith(('.json', '.JSON')):
        raise FileNotFoundError("Destination isn't a correct JSON file")

    src = pathlib.Path(ALERT_DB_PATH).as_posix()

    logging.debug("export alerts src path: " + src)
    logging.debug("export alerts dest path: " + dest)
    shutil.copy(src, dest)  # raises SameFileError


def get_default_config(key, cmd="str"):
    """Read the configuration file and return the value for the given key

    The cmd attribute defines the type of the value. Default is str.

    Attributes:
        key: The key of the key-value pair in the config file
        cmd: Type of the desired value. Default is str.

    Exceptions:
        KeyError: Is the key doesn't match any key in the config file.
        configparser.NoSectionError: If the config file or the section doesn't exist.

    """
    config = configparser.RawConfigParser()
    config.read(DEFAULT_CONFIG_PATH)  # load the file in the parser
    try:
        if cmd == "int":
            value = config.getint("default", key)
        elif cmd == "bool":
            value = config.getboolean("default", key)
        else:
            value = config.get("default", key)
    except configparser.NoOptionError as e:
        raise KeyError(e)  # key not found

    logging.debug("default config load(key,value): (" + key + ";" + str(value) + ")")
    return value


def set_default_config(key, value):
    """ Set the given (key,value) pair in the config file.

    Preserves the Caps

    Attributes:
        key: the key
        value: the value

    Exceptions:
        configparser.NoSectionError: If the config file or the section doesn't exist.

    """
    config = configparser.RawConfigParser()
    config.optionxform = str  # preserve the Caps in the config file
    config.read(DEFAULT_CONFIG_PATH)  # load the config file in the parser
    config.set("default", key, str(value))  # update the parser
    with open(DEFAULT_CONFIG_PATH, 'w') as configfile:
        config.write(configfile)  # write back the parser in the config file

    logging.debug("default config set(key,value): (" + key + ";" + str(value) + ")")
