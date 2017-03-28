from Alert import Alert

class SimpleAlert(Alert):

    def __init__(self, time, message):
        super(SimpleAlert, self).__init__(time)
        self._message = message

    def triggered(self):
        #todo
        print("display notification" + " " + self._message + " " + str(self._time))