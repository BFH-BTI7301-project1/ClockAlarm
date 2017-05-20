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

from _clockalarm import Alert


class SimpleAlert(Alert):
    """Simple Alert implementation with text message

    Attributes:
        trigger_time: The time at which the alert is triggered.
        notification: The notification to display when the alert is triggered.
        periodicity: frequency in which the alert is displayed, in seconds.
    """

    def __init__(self, trigger_time, notification, periodicity=None):
        """Default constructor for the SimpleAlert class."""
        super(SimpleAlert, self).__init__(trigger_time)
        self.notification = notification
        self.periodicity = periodicity

    def get_periodicity(self):
        """Get the SimpleAlert periodicity

        Returns:
            The periodicity
        """
        return self.periodicity

    def get_notification(self):
        """Get the Notification

        Returns:
            The Notification of the Alert
        """
        return self.notification

    def triggered(self):
        """This method does the same as
        :func:`~_clockalarm.Alert.triggered`
        """
        self.timeout.emit(self.notification)
