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

import abc

import PyQt5.QtCore as pyqt


class AlertMeta(type(pyqt.QObject), abc.ABC):
    """Abstract Metaclass inheriting QObject's metaclass"""
    pass


class Alert(pyqt.QObject, metaclass=AlertMeta):
    """Abstract Alert class representing alerts.

    Attributes:
        trigger_time: The trigger time of the alert.
        id: The identification number of the alert in the alert.
        Set up when added to the database.
    """

    timeout = pyqt.pyqtSignal('PyQt_PyObject')

    def __init__(self, trigger_time):
        """Inits Alert class with the trigger time given in arguments."""
        super(Alert, self).__init__()
        self.trigger_time = trigger_time
        self.id = None

    def get_id(self):
        """Get the Alert identifier.

        Returns:
            The identifier of the alert.
        """
        return self.id

    def get_trigger_time(self):
        """Get the Alert trigger time in seconds since epoch.

        Returns:
            The trigger time
        """
        return self.trigger_time

    @abc.abstractmethod
    def triggered(self):
        """Triggers the alert action."""
        return
