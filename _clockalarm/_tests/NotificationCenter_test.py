from os.path import join, dirname, abspath

import pytest
from PyQt5.Qt import QRect, QApplication

from _clockalarm import Notification
from _clockalarm import NotificationCenter
from _clockalarm.UI.NotificationWidget import NotificationWidget
from _clockalarm.utils import importExportUtils

app = QApplication([])


@pytest.fixture
def before():
    importExportUtils.DEFAULT_CONFIG_PATH = join(dirname(abspath(__file__)), "config_test.cfg")
    importExportUtils.ALERT_DB_PATH = join(dirname(abspath(__file__)), "alertsDB_test.json")


class FakeParent(object):
    MUTE = False


@pytest.mark.test
def test_notification_center_constructor(before):
    """Test the :class:`~_clockalarm.NotificationCenter` constructor.

    Test the correctness of the variable initialization.

    """
    screen_geometry = QRect(0, 0, 1920, 1080)
    fake_parent = FakeParent()
    notification_center = NotificationCenter.NotificationCenter(screen_geometry, fake_parent)

    assert notification_center.parent == fake_parent
    assert notification_center._screen_geometry == screen_geometry
    assert notification_center._max_popups == 4
    assert len(notification_center._popup_queue) == 0
    assert len(notification_center._displayed_popups) == 0
    assert notification_center._lock.acquire()
    assert notification_center.ax == 1550
    assert notification_center.ay == 43

    nc = NotificationCenter.NotificationCenter(screen_geometry)
    assert nc.parent is None


@pytest.mark.test
def test_nc_add_to_queue(before):
    """Test the :class:`~_clockalarm.NotificationCenter` add_to_queue method.

    After one notification is added to the list, the queue is empty and one popup is displayed.

    """

    nc = NotificationCenter.NotificationCenter(QRect(0, 0, 1920, 1080), FakeParent)
    noti_1 = Notification("test message")
    nc.add_to_queue(noti_1)

    assert len(nc._popup_queue) == 0
    assert len(nc._displayed_popups) == 1
    assert nc._displayed_popups[0].notification.get_message() == "test message"


@pytest.mark.test
def test_nc_add_to_queue_multiple(before):
    """Test the :class:`~_clockalarm.NotificationCenter` add_to_queue method.

    After 6 notifications are added to the list, 2 elements in the queue and 4 popups displayed.

    """

    nc = NotificationCenter.NotificationCenter(QRect(0, 0, 1920, 1080), FakeParent)
    for i in range(0, 6):
        nc.add_to_queue(Notification("test message " + str(i)))

    assert len(nc._popup_queue) == 2
    assert len(nc._displayed_popups) == 4


@pytest.mark.test
def test_nc_add_to_queue_error(before):
    """Test the :class:`~_clockalarm.NotificationCenter` add_to_queue method.

    Wrong argument passed to the add_to_queue method.

    """

    nc = NotificationCenter.NotificationCenter(QRect(0, 0, 1920, 1080))

    with pytest.raises(ValueError):
        nc.add_to_queue(None)
    with pytest.raises(ValueError):
        nc.add_to_queue(QRect())


@pytest.mark.test
def test_nc_close_popup(before):
    """Test the :class:`~_clockalarm.NotificationCenter` close_popup method.

    Test that the popup is correctly removed from the list when method is called

    """

    nc = NotificationCenter.NotificationCenter(QRect(0, 0, 1920, 1080), FakeParent())
    nc.add_to_queue(Notification("test message"))

    assert len(nc._displayed_popups) == 1
    popup = nc._displayed_popups[0]
    nc.close_popup(popup)
    assert len(nc._displayed_popups) == 0


@pytest.mark.test
def test_nc_close_popup_wrong_arg(before):
    """Test the :class:`~_clockalarm.NotificationCenter` close_popup method.

    Trying to remove None or wrong NotificationWidget object

    """

    nc = NotificationCenter.NotificationCenter(QRect(0, 0, 1920, 1080), FakeParent())
    nc.add_to_queue(Notification("test message"))

    with pytest.raises(ValueError):
        nc.close_popup(None)
    with pytest.raises(ValueError):
        nc.close_popup(QRect)
    assert len(nc._displayed_popups) == 1


@pytest.mark.test
def test_nc_close_popup_nonexistent_popup(before):
    """Test the :class:`~_clockalarm.NotificationCenter` close_popup method.

    Trying to remove NotificationWidget object not on the list.

    """

    geometry = QRect(0, 0, 1920, 1080)
    nc = NotificationCenter.NotificationCenter(QRect(0, 0, 1920, 1080), FakeParent())
    nc.add_to_queue(Notification("test message"))

    with pytest.raises(KeyError):
        nc.close_popup(NotificationWidget(geometry, Notification("message")))
    assert len(nc._displayed_popups) == 1


@pytest.mark.test
def test_nc_refresh(before):
    """Test the :class:`~_clockalarm.NotificationCenter` refresh method."""

    nc = NotificationCenter.NotificationCenter(QRect(0, 0, 1920, 1080), FakeParent())
    for i in range(0, 6):
        nc.add_to_queue(Notification("test message " + str(i)))
    nc.refresh()
    assert len(nc._popup_queue) == 2
    assert len(nc._displayed_popups) == 4


@pytest.mark.test
def test_nc_display_popup(before):
    """Test the :class:`~_clockalarm.NotificationCenter` display_popup method."""

    nc = NotificationCenter.NotificationCenter(QRect(0, 0, 1920, 1080), FakeParent())
    for i in range(0, 4):
        nc.display_popup(QRect(0, 0, 1920, 1080), Notification("Test Message" + str(i)))

    assert len(nc._displayed_popups) == 4


@pytest.mark.test
def test_nc_display_popup_index_error(before):
    """Test the :class:`~_clockalarm.NotificationCenter` display_popup method.

    Too much popups are added to the display zone

    """

    nc = NotificationCenter.NotificationCenter(QRect(0, 0, 1920, 1080), FakeParent())
    with pytest.raises(IndexError):
        for i in range(0, 5):
            nc.display_popup(QRect(0, 0, 1920, 1080), Notification("Test Message" + str(i)))


@pytest.mark.test
def test_nc_display_popup_value_error(before):
    """Test the :class:`~_clockalarm.NotificationCenter` display_popup method.

    Wrong arguments are passed to the method

    """

    nc = NotificationCenter.NotificationCenter(QRect(0, 0, 1920, 1080), FakeParent())
    with pytest.raises(ValueError):
        nc.display_popup(None, Notification("Test Message"))
    with pytest.raises(ValueError):
        nc.display_popup(QRect(0, 0, 1920, 1080), None)
    with pytest.raises(ValueError):
        nc.display_popup(0, Notification("Test Message"))
    with pytest.raises(ValueError):
        nc.display_popup(QRect(0, 0, 1920, 1080), 0)
