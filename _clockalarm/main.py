import sys
import time
from _clockalarm.NotificationCenter import NotificationCenter
from _clockalarm.SimpleAlert import SimpleAlert


def main(argv):

    nc = NotificationCenter()  # to manage multiple notifications

    """2 test alerts"""
    SimpleAlert(time.time() + 3, "This message is delayed (3sec)", nc)
    SimpleAlert(time.time() + 5, "This message is delayed (5sec)", nc)

if __name__ == '__main__':
    main(sys.argv)
