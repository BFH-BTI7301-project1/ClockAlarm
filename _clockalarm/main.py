import sys
from _clockalarm.SimpleAlert import SimpleAlert


def main(argv):
    sa = SimpleAlert(60, "My message")
    sa.triggered()

if __name__ == '__main__':
    main(sys.argv)
