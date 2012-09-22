import sys, json
from PySide.QtCore import *
from PySide.QtGui import *
from couchdbcurl import Server 
from UI.UI_ReplicationWindow import *


class ReplicationWindow(QDialog):
    def __init__(self,mainWindow, server):
        super(ReplicationWindow, self).__init__()
        self.ui = Ui_ReplicationWindow()
        self.ui.setupUi(self)
        self.mainWindow = mainWindow
        self.server = server
        self.serv_obj = Server(str(self.server['url']))
        self.ui.btn_save.clicked.connect(self.add_react)
        db_names = []       
        for db in self.serv_obj:
            db_names.append(db)
        db_names.sort()
        for i, value in enumerate(db_names):
            self.ui.cmb_localsource.addItem(value, userData=value)
            self.ui.cmb_localtarget.addItem(value, userData=value)

    def add_react(self): 
        if self.validate():
            if self.ui.rdb_localsource.isChecked():
                source = str(self.ui.cmb_localsource.currentText())
            else:
                source = str(self.ui.txt_remotesource.text())
            if self.ui.cbx_create_target.isChecked():
                target = str(self.ui.txt_createtarget.text())
                create_target = True
            else:
                create_target = False
                if self.ui.rdb_localtarget.isChecked():
                    target = str(self.ui.cmb_localtarget.currentText())
                else:
                    target = str(self.ui.txt_remotetarget.text())
            if source.startswith("http"):
                if not source.endswith("/"):
                    source += "/"
            if target.startswith("http"):
                if not target.endswith("/"):
                    target += "/"    
            if self.ui.cbx_persistent.isChecked():
                replication_id = str(self.ui.txt_name.text())
                user_ctx = json.loads(self.ui.txt_userctx.text())
                if self.ui.cbx_continuous.isChecked():
                    continuous = True 
                else:
                    continuous = False
                replicator_db = self.serv_obj['_replicator']
                new_replication = {'source': source, 'target': target, 'continuous': continuous, 'user_ctx': user_ctx, 'create_target': create_target}
                if replication_id:
                    try:
                        replicator_db[replication_id] = new_replication
                    except: 
                        QMessageBox(QMessageBox.Warning, 'Error', 'Error: %s' % (sys.exc_value), QtGui.QMessageBox.Ok).exec_()
                else:
                    try:
                        replicator_db.create(new_replication)
                    except:
                        QMessageBox(QMessageBox.Warning, 'Error', 'Error: %s' % (sys.exc_value), QtGui.QMessageBox.Ok).exec_()
            else:
                new_replication = {'source': source, 'target': target}
                if new_replication in self.server.get('replications'):
                    QMessageBox(QMessageBox.Warning, 'Warning', 'Record for this replication already exist.', QtGui.QMessageBox.Ok).exec_()
                else:
                    self.mainWindow.dump_replication_record(self.server, new_replication)
            self.close()
            
            
    def validate(self):
        if not self.ui.rdb_localsource.isChecked() and not str(self.ui.txt_remotesource.text()):
            QMessageBox(QMessageBox.Critical, 'Error', 'Source field are required.', QtGui.QMessageBox.Ok).exec_()
            return False
        if not self.ui.rdb_localtarget.isChecked() and not str(self.ui.txt_remotetarget.text()):
            QMessageBox(QMessageBox.Critical, 'Error', 'Target field are required.', QtGui.QMessageBox.Ok).exec_()
            return False
        if self.ui.cbx_persistent.isChecked():
            try:
                json.loads(str(self.ui.txt_userctx.text()))
            except ValueError:
                QMessageBox(QMessageBox.Critical, 'Error', 'User_ctx is not in json format.', QtGui.QMessageBox.Ok).exec_()
                return False
        return True
            
            
    def closeEvent(self,event):
        try:
            self.mainWindow.replication_windows.remove(self)
        except:
            #print "error removing from replication windows list"
            logging.debug('ReplicationWindow: error removing from replication windows list')
            
