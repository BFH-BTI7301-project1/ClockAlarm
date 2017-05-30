import configparser
import filecmp
import os
from os.path import join, dirname, abspath
from shutil import SameFileError, copy

import pytest

from _clockalarm.utils import importExportUtils


@pytest.fixture(scope='module')
def init_paths():
    importExportUtils.DEFAULT_CONFIG_PATH = join(dirname(abspath(__file__)), "config_test.cfg")
    importExportUtils.ALERT_DB_PATH = join(dirname(abspath(__file__)), "alertsDB_test.json")


@pytest.mark.test
def test_import_alert_wrong_file():
    """Test the :class:`~_clockalarm.utils.importExportUtils` import_alerts_file method.

    Src file is None or wrong

    """
    with pytest.raises(FileNotFoundError):
        importExportUtils.import_alerts_file(None)
    with pytest.raises(FileNotFoundError):
        importExportUtils.import_alerts_file(dirname(abspath(__file__)))  # exists but not json
    with pytest.raises(FileNotFoundError):
        importExportUtils.import_alerts_file("not/a/path.json")


@pytest.mark.test
def test_export_alert_wrong_file():
    """Test the :class:`~_clockalarm.utils.importExportUtils` export_alerts_file method.

    Dest file is None or wrong

    """
    with pytest.raises(FileNotFoundError):
        importExportUtils.export_alerts_file(None)
    with pytest.raises(FileNotFoundError):
        importExportUtils.export_alerts_file(dirname(abspath(__file__)))  # not json


@pytest.mark.test
def test_import_alert_same_file():
    """Test the :class:`~_clockalarm.utils.importExportUtils` import_alerts_file method.

    Src and Dest file are the same

    """
    src = importExportUtils.ALERT_DB_PATH
    with pytest.raises(SameFileError):
        importExportUtils.import_alerts_file(src)


@pytest.mark.test
def test_export_alert_same_file():
    """Test the :class:`~_clockalarm.utils.importExportUtils` export_alerts_file method.

    Src and Dest file are the same

    """
    dest = importExportUtils.ALERT_DB_PATH
    with pytest.raises(SameFileError):
        importExportUtils.export_alerts_file(dest)


@pytest.mark.test
def test_export_alert():
    """Test the :class:`~_clockalarm.utils.importExportUtils` export_alerts_file method."""
    dest = join(dirname(abspath(__file__)), "alertsDB_test_2.json")
    importExportUtils.export_alerts_file(dest)

    assert filecmp.cmp(importExportUtils.ALERT_DB_PATH, dest)

    os.remove(dest)  # clean the exported file


@pytest.mark.test
def test_import_alert():
    """Test the :class:`~_clockalarm.utils.importExportUtils` export_alerts_file method."""
    src = join(dirname(abspath(__file__)), "alertsDB_test_2.json")
    copy(importExportUtils.ALERT_DB_PATH, src)  # copy the test db

    importExportUtils.import_alerts_file(src)

    assert filecmp.cmp(importExportUtils.ALERT_DB_PATH, src)

    os.remove(src)  # clean the exported file


@pytest.mark.test
def test_get_default_config():
    """Test the :class:`~_clockalarm.utils.importExportUtils` get_default_config method."""
    assert importExportUtils.get_default_config('NOTIFICATION_COLOR_HEX') == '#ff5500'
    assert importExportUtils.get_default_config('NOTIFICATION_FONT_SIZE', 'int') == 27
    assert importExportUtils.get_default_config('MUTE', 'bool')


@pytest.mark.test
def test_get_default_config_nonexistent_key():
    """Test the :class:`~_clockalarm.utils.importExportUtils` get_default_config method.

    The key doesn't exist in the config file

    """
    with pytest.raises(KeyError):
        importExportUtils.get_default_config('SOME_KEY')


@pytest.mark.test
def test_get_default_config_nonexistent_file():
    """Test the :class:`~_clockalarm.utils.importExportUtils` get_default_config method.

    The configuration file doesn't exists

    """
    tmp = importExportUtils.DEFAULT_CONFIG_PATH
    importExportUtils.DEFAULT_CONFIG_PATH = 'corrupted'
    with pytest.raises(configparser.NoSectionError):
        assert importExportUtils.get_default_config('MUTE', 'bool')
    importExportUtils.DEFAULT_CONFIG_PATH = tmp  # restore the config file path


@pytest.mark.test
def test_set_default_config():
    """Test the :class:`~_clockalarm.utils.importExportUtils` set_default_config method."""
    importExportUtils.set_default_config('NOTIFICATION_FONT_SIZE', 25)
    assert importExportUtils.get_default_config('NOTIFICATION_FONT_SIZE', 'int') == 25

    importExportUtils.set_default_config('NOTIFICATION_FONT_SIZE', 27)  # restore the test config file


@pytest.mark.test
def test_set_default_config_nonexistent_file():
    """Test the :class:`~_clockalarm.utils.importExportUtils` set_default_config method.

    Config file path is incorrect.

    """
    tmp = importExportUtils.DEFAULT_CONFIG_PATH
    importExportUtils.DEFAULT_CONFIG_PATH = 'corrupted'

    with pytest.raises(configparser.NoSectionError):
        importExportUtils.set_default_config('NOTIFICATION_FONT_SIZE', 25)

    importExportUtils.DEFAULT_CONFIG_PATH = tmp  # restore the config file path
