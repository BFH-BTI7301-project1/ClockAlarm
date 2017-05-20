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

from PyQt5.QtCore import pyqtSignal, QThread


class Clock(QThread):
    """Clock emitting ticks with a given periodicity.

    The class extends QThread to allow threading.

    Attributes:
        frequency: The frequency at which the clock emits a tick.
        parent: The parent. Default value is None.
    """
    tick = pyqtSignal('PyQt_PyObject')

    def __init__(self, frequency, parent=None):
        """Default constructor for the Clock class."""
        super(self.__class__, self).__init__(parent)
        self._frequency = frequency
        self.running = True

    def run(self):
        """Start the clock."""
        while self.running:
            self.sleep(self._frequency)
            self.tick.emit(time.time())
            logging.log(1, "clocktread tick(P=" + str(self._frequency) + "s)")

    def stop(self):
        """Stop the clock."""
        self.running = False
