from os.path import dirname, abspath, join

from _clockalarm import main

test_config_path = join(dirname(abspath(__file__)), "config_test.cfg")
test_alertsDB_path = join(dirname(abspath(__file__)), "alertsDB_test.json")


def test_app_constructor():
    """Tests the :class:`~_clockalarm.main.App` constructor.
    
    """
    argv = ["file", test_config_path, test_alertsDB_path]
    main.App(argv[1], argv[2], argv)
