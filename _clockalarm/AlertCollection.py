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

import logging
import time

from tinydb import TinyDB, Query

from _clockalarm import Notification
from _clockalarm.SimpleAlert import SimpleAlert
from _clockalarm.utils import importExportUtils


class AlertCollection(object):
    """Collection of all the Alert objects running on the program.

    This class contains utilities to load, update and save the alerts in a TinyDB database, and maintain the correct
    state of all the alerts

    """

    def __init__(self, parent=None):
        """Default constructor for AlertCollection object

        Attributes:
            parent (main.App, optional): Parent of the class

        Exceptions:
            ValueError: If the parent argument is not None but isn't an instance of _clockalarm.main.App

        """
        super(self.__class__, self).__init__()

        import _clockalarm.main
        if parent and not isinstance(parent, _clockalarm.main.App):
            raise ValueError("parent argument is set but isn't an instance of _clockalarm.main.App")

        self.parent = parent
        self.db = TinyDB(importExportUtils.ALERT_DB_PATH, default_table="alerts")  # open the DB or create a new one
        self.alert_list = []

        self.clean_db()  # search for outdated or duplicated alerts in DB
        self.load_db()  # load the TinyDB in AlertCollection object

        self.display()

    def add(self, alert: SimpleAlert):
        """Add the Alert given in argument to the collection of alerts

        If parent is set, the new Alert is connected to the notification center and the list of displayed alerts is
        updated.

        Attributes:
            alert(SimpleAlert): The alert to add to the collection

        Exceptions:
            ValueError: If the alert argument is None or incorrect.

        """
        if alert is None or not isinstance(alert, SimpleAlert):
            raise ValueError('None or incorrect alert argument')

        self.alert_list.append(alert)
        if self.parent:  # connect the timeout signal to the notification center
            alert.timeout.connect(self.parent.notification_center.add_to_queue)

        alert.id = self.db.insert(  # update the TinyDB
            {'trigger_time': alert.trigger_time,
             'message': alert.get_notification().get_message(),
             'color_hex': alert.notification.color_hex,
             'font_family': alert.notification.font_family,
             'font_size': alert.notification.font_size,
             'sound': alert.notification.sound,
             'periodicity': alert.periodicity})
        self.display()

    def edit(self, id_alert: int, notification: Notification = None,
             trigger_time: int = None, periodicity: int = None):
        """Update an alert with the given modifications

        If the trigger_time is in the past, he won't re updated.

        Attributes:
            id_alert(int): The id number of the alert to modify
            notification(Notification, optional): Default is None. The new notification
            trigger_time(int,optional): Default is None. The new trigger time
            periodicity(int,optional: Default is None. The new periodicity

        Exceptions:
            KeyError: If the alert to edit doesn't exist in the database.
            ValueError: If the periodicity argument is equal or under zero.

        """
        try:
            alert_to_edit = next(
                alert for alert in self.alert_list if alert.id == id_alert)  # raises StopIteration exception
        except StopIteration as e:
            raise KeyError(e)

        if alert_to_edit:
            if notification:
                alert_to_edit.notification = notification
                self.db.update({'message': notification.message,
                                'color_hex': notification.color_hex,
                                'font_family': notification.font_family,
                                'font_size': notification.font_size,
                                'sound': notification.sound}, eids=[id_alert])
            if periodicity is not None:
                if periodicity <= 0:
                    raise ValueError("Periodicity have to be greater than 0")
                alert_to_edit.periodicity = periodicity
                self.db.update({'periodicity': alert_to_edit.periodicity},
                               eids=[id_alert])
            if trigger_time is not None:
                if trigger_time < time.time():
                    logging.error("alert can't be triggered in the past")
                else:
                    alert_to_edit.trigger_time = trigger_time
                    self.db.update({'trigger_time': alert_to_edit.trigger_time}, eids=[id_alert])
            self.display()

    def delete(self, id_alert: int):
        """Remove an alert from the collection

        Attributes:
            id_alert: The id number of the alert to remove.

        Exceptions:
            KeyError: If the alert to delete doesn't exist in the database.

        """
        self.alert_list = [alert for alert in self.alert_list
                           if alert.id != id_alert]
        self.db.remove(eids=[id_alert])
        self.display()

    def check_timers(self, trig_time):
        """Check all the alerts to see if on should be triggered

        This function is triggered periodically by the clock.

        Attributes:
            trig_time: Actual time, in seconds.

        """
        for alert in self.alert_list:
            if trig_time >= alert.trigger_time:
                alert.triggered()
                if not alert.periodicity:
                    self.delete(alert.get_id())
                else:
                    self.edit(alert.get_id(), trigger_time=alert.get_trigger_time() + alert.get_periodicity())

    def display(self):
        """Actualize the UI alert list display

        If parent is unset, the AlertCollection object isn't link to any QWindow and nothing append

        """
        if self.parent:
            self.parent.main_window.alert_list_widget.actualize(self.alert_list)

    def load_db(self):
        """Fill the AlertCollection with Alerts form the TinyDB database

        Exceptions:
            IOError: If a required parameter can't be found in the database. The database is probably corrupted.

        """
        self.alert_list = []  # clean the alert list
        for alert in self.db.all():
            try:
                notification = Notification(alert["message"],
                                            color_hex=alert["color_hex"],
                                            font_family=alert["font_family"],
                                            font_size=alert["font_size"],
                                            sound=alert["sound"])
                new_alert = SimpleAlert(alert["trigger_time"], notification)
            except KeyError as e:
                raise IOError('The alert database seems corrupted' + str(e))

            if "periodicity" in alert:  # periodicity can not appear in db
                new_alert.periodicity = alert["periodicity"]
            new_alert.id = alert.eid  # use the TinyDB object eid as alert id

            self.alert_list.append(new_alert)
            if self.parent:  # connect the alert to the GUI
                new_alert.timeout.connect(self.parent.notification_center.add_to_queue)

    def clean_db(self):
        """Make the TinyDB database consistent

        All the outdated alerts without periodicity are removed.
        New trigger time is calculated for outdated alerts with periodicity.

        If the db is corrupted, nothing append.
        """

        def operation():  # to apply on alerts with periodicity
            def transform(element):
                if element['periodicity']:  # periodicity not None
                    trig = element['trigger_time']
                    while trig < time.time():  # add periodicity value to trigger time until the alert occurs in the future
                        trig += element['periodicity']
                    element['trigger_time'] = trig

            return transform

        alert_query = Query()
        self.db.update(operation(), alert_query.periodicity.exists())  # update trigger time
        self.db.remove(alert_query.trigger_time <= time.time())  # remove outdated
