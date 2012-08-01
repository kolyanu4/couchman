from PySide.QtCore import Qt
import os
from os.path import dirname, realpath


if not os.path.exists(os.path.expanduser('~/.config/couchman/')):
    os.makedirs(os.path.expanduser('~/.config/couchman/'))

dir_path = os.path.abspath(os.path.expanduser('~/.config/couchman/'))
DB_FILE_PATH = os.path.join(dir_path, 'couchman.json')
LOG_FILENAME = os.path.join(dir_path, 'couchman.log')
DATE_FORMAT = '%Y-%m-%d %H:%M:%S'
DATETIME_FMT = '%Y-%m-%d %H:%M:%S'
INFINITY = 360 * 24 * 60
ROOT_DIR = dirname(realpath(__file__))
SERVER_INFO_ROLE = Qt.UserRole + 1
TASK_INFO_ROLE =  Qt.UserRole + 2
VIEW_INFO_ROLE =  Qt.UserRole + 3



