from PySide.QtCore import *
from PySide.QtGui import *


class WorkerListTreeModel(QAbstractTableModel):
    def __init__(self, workers, parent = None):
        QAbstractTableModel.__init__(self, parent)
        self.workers = workers
        self.headers = ("Server Name", "Last message from worker", "Type")

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
                    if 'last_message' in str(self.workers[index.row()]):
                        return str(self.workers[index.row()]['last_message']) 
                    else:
                        return "-"
            if index.column() == 2:
                if not 'stop' in str(self.workers[index.row()]['thread']):
                    return str(self.workers[index.row()]['command'])
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
        self.resize(750,400)
        self.mainwindow = mainWindow
        self.setWindowTitle("Workers List")
        self.workers_table = QTreeView()
        self.workers_table.setItemsExpandable(False)
        self.workers_table.setExpandsOnDoubleClick(False)
        self.workers_table.setRootIsDecorated(False)
        self.workers_list_model = WorkerListTreeModel(self.mainwindow.workers)
        self.workers_table.setModel(self.workers_list_model)
        for i in range(self.workers_list_model.columnCount()):
            self.workers_table.resizeColumnToContents(i) 
        layout = QHBoxLayout()
        layout.addWidget(self.workers_table)
        self.setLayout(layout)
