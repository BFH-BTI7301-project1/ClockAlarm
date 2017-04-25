import time

from tinydb import TinyDB, Query

from _clockalarm import SimpleAlert, Notification
from _clockalarm import main


class AlertCollection:
    alert_list = []
    db = TinyDB('../alertsDB.json', default_table="alerts")

    def __init__(self, nc):
        super(self.__class__, self).__init__()
        self._notification_center = nc
        self.clean_db()
        self.load_db()
        self.display()

    def add(self, alert: SimpleAlert):
        self.alert_list.append(alert)
        alert.timeout.connect(self._notification_center.add_to_queue)
        alert.id = self.db.insert(
            {'trigger_time': alert.trigger_time, 'message': alert.get_identifier(), 'periodicity': alert.periodicity})
        self.display()

    def edit(self, notification: Notification, trigger_time: int, id_alert: int, periodicity: int = None):
        alert_to_edit = next(alert for alert in self.alert_list if alert.id == id_alert)
        if alert_to_edit:
            alert_to_edit._notification = notification
            alert_to_edit.periodicity = periodicity
            alert_to_edit.trigger_time = trigger_time
            self.db.update({'trigger_time': alert_to_edit.trigger_time, 'message': alert_to_edit.get_identifier(),
                            'periodicity': alert_to_edit.periodicity}, eids=[id_alert])
            self.display()

    def delete(self, id_alert: int):
        self.alert_list = [alert for alert in self.alert_list if alert.id != id_alert]
        self.db.remove(eids=[id_alert])
        self.display()

    def check_timers(self, trig_time):
        for alert in self.alert_list:
            if trig_time >= alert.trigger_time:
                alert.triggered()

    def display(self):
        main.app.main_window.alert_list_widget.actualize(self.alert_list)

    def load_db(self):
        for alert in self.db.all():
            new_alert = SimpleAlert.SimpleAlert(alert["trigger_time"], alert["message"])
            if "periodicity" in alert:
                new_alert.periodicity = alert["periodicity"]
            new_alert.id = alert.eid

            self.alert_list.append(new_alert)
            new_alert.timeout.connect(self._notification_center.add_to_queue)

        """FAKE DB"""
        alert_10 = SimpleAlert.SimpleAlert(time.time() + 10, "This message is delayed: 10 seconds")
        self.add(alert_10)
        alert_3 = SimpleAlert.SimpleAlert(time.time() + 3, "This message is delayed: 3 seconds", None)
        self.add(alert_3)
        alert_60 = SimpleAlert.SimpleAlert(time.time() + 60, "This message is delayed: 60 seconds")
        self.add(alert_60)

    def save_db(self):
        self.db.purge()
        for alert in self.alert_list:
            self.db.insert({'trigger_time': alert.trigger_time, 'message': alert.get_identifier(),
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
