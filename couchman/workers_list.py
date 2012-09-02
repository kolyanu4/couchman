from PySide.QtCore import *
from PySide.QtGui import *
from UI.UI_WorkersWindow import *

class WorkerListTreeModel(QAbstractTableModel):
    def __init__(self, workers, parent = None):
        QAbstractTableModel.__init__(self, parent)
        self.workers = workers
        self.headers = ("Server Name", "Last Command", "Sent Date", "Received Command", "Received Date", "Worker")

    def columnCount(self, parent=None):
        return len(self.headers)
        
    def rowCount(self, parent=QModelIndex()):
        i = 0
        for j in self.workers: 
            if not 'stop' in str(j): 
                i += 1
        return i

    def data(self, index, role):
        if not index.isValid():
            return None
        if role == Qt.DisplayRole:
            if index.column() == 0:
                if not 'stop' in str(self.workers[index.row()]['thread']):
                    return str(self.workers[index.row()]['name'])
            if index.column() == 1:
                if not 'stop' in str(self.workers[index.row()]['thread']):
                    if 'send_command' in str(self.workers[index.row()]):
                        return str(self.workers[index.row()]['send_command']) 
                    else:
                        return "-"
            if index.column() == 2:
                if not 'stop' in str(self.workers[index.row()]['thread']):
                    if 'send_date' in str(self.workers[index.row()]):
                        return str(self.workers[index.row()]['send_date']) 
                    else:
                        return "-"
            if index.column() == 3:
                if not 'stop' in str(self.workers[index.row()]['thread']):
                    if 'rec_command' in str(self.workers[index.row()]):
                        return str(self.workers[index.row()]['rec_command']) 
                    else:
                        return "-"
            if index.column() == 4:
                if not 'stop' in str(self.workers[index.row()]['thread']):
                    if 'last_rec_message' in str(self.workers[index.row()]):
                        return str(self.workers[index.row()]['last_rec_message']) 
                    else:
                        return "-"
            if index.column() == 5:
                if not 'stop' in str(self.workers[index.row()]['thread']):
                    return '%s worker' % str(self.workers[index.row()]['type'])
        return None
        
    def headerData(self, column, orientation, role):
        if (orientation == Qt.Horizontal and role == Qt.DisplayRole):
            try:
                return self.headers[column]
            except IndexError:
                pass
        return None

    def update_data(self):
        self.sort(1,Qt.AscendingOrder)
        self.emit(SIGNAL('layoutChanged()'))
        self.emit(SIGNAL('dataChanged(const QModelIndex &, const QModelIndex &)'), self.index(0,0), self.index(self.rowCount(),self.columnCount()))


class WorkerListManager(QWidget):

    def __init__(self, mainWindow):
        super(WorkerListManager, self).__init__()
        self.ui = Ui_WorkersWindow()
        self.ui.setupUi(self)
        self.mainwindow = mainWindow
        self.workers_list_model = WorkerListTreeModel(self.mainwindow.workers)
        self.ui.workers_table.setModel(self.workers_list_model)
        for i in range(self.workers_list_model.columnCount()):
            self.ui.workers_table.resizeColumnToContents(i)
