.. ClockAlarm documentation master file, created by
   sphinx-quickstart on Sun May 14 18:47:08 2017.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

ClockAlarm: a cross-platform alarm manager
==========================================

ClockAlarm is a cross-platform (linux, Windows, macOS) alarm manager that will
help you improve your life organization. Define alerts and never miss events
again.

Features
--------

* Simple / Periodic alerts
* Works on Windows, macOS and Linux 
* Safe, corrupt-free and humanly readable database
* Fully customizable alerts (sound, color, font, etc)

Installation
------------

You will need a working python environment.

Requirements
~~~~~~~~~~~~

* python => 3.6
* pygame => 1.9.3
* PyQt5 => 5.8.2
* sip => 4.19.2
* tinydb => 3.2.2

You can install these packages using the following command::

    $ pip3 install pygame pyqt5 sip tinydb

Clone the repository::

    $ git clone https://github.com/BFH-BTI7301-project1/ClockAlarm.git

Launch ClockAlarm::

    $ python3 bin/clockalarm&

Development
-----------

Requirements
~~~~~~~~~~~~

* coverage >= 4.4.1
* pytest >= 3.0.7
* pytest-cov >= 2.5.1
* pytest-qt >= 2.1.0
* pytest-catchlog >= 1.2.2
* coveralls >= 1.1

You can install these packages using the following command::

    $ pip3 install -r stable-req.txt

Run the tests::
    
    $ py.test --cov-report term --cov=. _clockalarm/_tests --no-xvfb

`GitHub project page <https://github.com/BFH-BTI7301-project1/ClockAlarm>`_

Bugs/Requests
-------------

Please use the `GitHub issue tracker <https://github.com/BFH-BTI7301-project1/
ClockAlarm/issues>`_ to submit bugs or request features.


ClockAlarm API
--------------

.. toctree::
   :maxdepth: 4

   modules

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
