import time

from tinydb import TinyDB, Query

from _clockalarm import SimpleAlert
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
        alert.timeout.connect(self._notification_center.display)
        self.db.insert({'trigger_time': alert.trigger_time, 'message': alert.get_identifier()})
        self.display()

    def check_timers(self, trig_time):
        for alert in self.alert_list:
            if trig_time >= alert.trigger_time:
                alert.triggered()
                self.alert_list.remove(alert)
                alert.kill()
                self.display()

    def display(self):
        main.app.main_window.alert_list_widget.actualize(self.alert_list)

    def load_db(self):
        for alert in self.db.all():
            new_alert = SimpleAlert(alert["trigger_time"], alert["message"])
            self.alert_list.append(new_alert)
            new_alert.timeout.connect(self._notification_center.display)

        """FAKE DB"""
        alert_10 = SimpleAlert(time.time() + 10, "This message is delayed: 10 seconds")
        self.add(alert_10)
        alert_3 = SimpleAlert(time.time() + 3, "This message is delayed: 3 seconds")
        self.add(alert_3)
        alert_60 = SimpleAlert(time.time() + 60, "This message is delayed: 60 seconds")
        self.add(alert_60)

    def save_db(self):
        self.db.purge()
        for alert in self.alert_list:
            self.db.insert({'trigger_time': alert.trigger_time, 'message': alert.get_identifier()})

    def clean_db(self):
        alert_query = Query()
        self.db.remove(alert_query.trigger_time <= time.time())
