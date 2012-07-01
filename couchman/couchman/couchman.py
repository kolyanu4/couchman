#!/usr/bin/env python
from PyQt4.QtCore import *
from PyQt4.QtGui import *
from main_window import MainWindow
import sys
from config import *
import logging

def run():
    logging.basicConfig(filename=LOG_FILENAME,level=logging.DEBUG)
    logging.debug('Main:Start Application')

    app = QApplication(sys.argv)
    mainWindow = MainWindow()
    
    
    mainWindow.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    print "couchman"

