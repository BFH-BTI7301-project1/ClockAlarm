import os.path
import pathlib
import time

from tinydb import TinyDB, Query

from _clockalarm import Notification
from _clockalarm import main
from _clockalarm.SimpleAlert import SimpleAlert


class AlertCollection(object):
    db_path = pathlib.Path(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))).as_posix() + '/alertsDB.json'
    db = TinyDB(db_path, default_table="alerts")

    def __init__(self, nc):
        super(self.__class__, self).__init__()
        self._notification_center = nc
        self.alert_list = []
        self.clean_db()
        self.load_db()
        self.display()

    def add(self, alert: SimpleAlert):
        self.alert_list.append(alert)
        alert.timeout.connect(self._notification_center.add_to_queue)
        alert.id = self.db.insert(
            {'trigger_time': alert.trigger_time, 'message': alert.get_notification().get_message(),
             'color_hex': alert.notification.color_hex, 'font_family': alert.notification.font_family,
             'font_size': alert.notification.font_size, 'sound': alert.notification.sound,
             'periodicity': alert.periodicity})
        self.display()

    def edit(self, id_alert: int, notification: Notification = None, trigger_time: int = None, periodicity: int = None):
        alert_to_edit = next(alert for alert in self.alert_list if alert.id == id_alert)
        if alert_to_edit:
            if notification:
                alert_to_edit.notification = notification
                self.db.update({'message': notification.message, 'color_hex': notification.color_hex,
                                'font_family': notification.font_family, 'font_size': notification.font_size,
                                'sound': notification.sound}, eids=[id_alert])
            if periodicity:
                alert_to_edit.periodicity = periodicity
                self.db.update({'periodicity': alert_to_edit.periodicity}, eids=[id_alert])
            if trigger_time:
                alert_to_edit.trigger_time = trigger_time
                self.db.update({'trigger_time': alert_to_edit.trigger_time}, eids=[id_alert])
            self.display()

    def delete(self, id_alert: int):
        self.alert_list = [alert for alert in self.alert_list if alert.id != id_alert]
        self.db.remove(eids=[id_alert])
        self.display()

    def check_timers(self, trig_time):
        for alert in self.alert_list:
            if trig_time >= alert.trigger_time:
                alert.triggered()
                if not alert.periodicity:
                    self.delete(alert.id)
                else:
                    self.edit(alert.id, trigger_time=alert.trigger_time + alert.periodicity)

    def display(self):
        main.app.main_window.alert_list_widget.actualize(self.alert_list)

    def load_db(self):
        for alert in self.db.all():
            notification = Notification(alert["message"], color_hex=alert["color_hex"],
                                        font_family=alert["font_family"], font_size=alert["font_size"],
                                        sound=alert["sound"])
            new_alert = SimpleAlert(alert["trigger_time"], notification)
            if "periodicity" in alert:
                new_alert.periodicity = alert["periodicity"]
            new_alert.id = alert.eid

            self.alert_list.append(new_alert)
            new_alert.timeout.connect(self._notification_center.add_to_queue)

    def save_db(self):
        self.db.purge()
        for alert in self.alert_list:
            self.db.insert({'trigger_time': alert.trigger_time, 'message': alert.get_notification().get_message(),
                            'font_family': alert.notification.font_family, 'font_size': alert.notification.font_size,
                            'color_hex': alert.notification.color_hex, 'sound': alert.notification.sound,
                            'periodicity': alert.periodicity})

    def clean_db(self):
        def operation():
            def transform(element):
                trig = element['trigger_time']
                while trig < time.time():
                    trig += element['periodicity']
                element['trigger_time'] = trig

            return transform

        alert_query = Query()
        self.db.update(operation(), alert_query.periodicity != None)
        self.db.remove(alert_query.trigger_time <= time.time())
