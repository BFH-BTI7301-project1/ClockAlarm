import sys
from PyQt5.QtWidgets import QApplication, QWidget
from PyQt5 import Qt

from SimpleAlert import SimpleAlert

def main(argv):

    sa = SimpleAlert(60, "My message")
    sa.triggered()
    """
    app = QApplication(sys.argv)

    icon = Qt.QIcon('resources/images/bfh_logo.png')

    w = QWidget()
    w.resize(250, 150)
    w.move(300, 300)
    w.setWindowIcon(icon)
    w.setWindowTitle('Simple')
    w.show()

    systemtray_icon = Qt.QSystemTrayIcon(app)
    systemtray_icon.setIcon(icon)
    systemtray_icon.show()
    systemtray_icon.showMessage('New notification', 'Display a message')
    sys.exit(app.exec_())
    """

if __name__ == '__main__':
    main(sys.argv)