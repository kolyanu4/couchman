#!/usr/bin/env python
import sys, logging
from PySide.QtCore import *
from PySide.QtGui import *
from main_window import MainWindow
from config import *

def main(argv=None):
    logging.basicConfig(filename=LOG_FILENAME,level=logging.DEBUG)
    logging.debug('Main:Start Application')

    app = QApplication(sys.argv)
    mainWindow = MainWindow()
    mainWindow.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    print "Type couchman to couchman"
    main()

