import multiprocessing, logging, sys
from datetime import datetime 
from PySide.QtCore import *
from PySide.QtGui import *
from couchdbcurl import Server 
from UI.UI_DocManager import *
from models import DBListModel, DBViewModel
from config import *
from workers import ViewWorker, DbWorker


class DBManager(QWidget):

    def __init__(self, server_view_list, mainWindow, server_list, selected_now):
        super(DBManager, self).__init__()
        self.ui = Ui_DocManager()
        self.ui.setupUi(self)
        self.close_action = QtGui.QAction(self)
        self.close_action.setShortcut(QKeySequence.Close)
        self.addAction(self.close_action)
        self.connect(self.close_action, SIGNAL("triggered()"), self, SLOT("close()"))
        self.win_name = self.windowTitle()
        self.setWindowTitle("%s - %s"%(self.win_name, selected_now['name']))
        self.mainWindow = mainWindow
        self.server_list = server_list
        self.server_view_list = server_view_list
        self.view_workers_list = []
        self.db_workers_list = []
        self.serv_db_list = []
        self.index = -1
        self.ui.tlw_db_list.setEnabled(False)
        self.ui.tlw_view_list.setEnabled(False)
        self.disabling_refresh()
        self.setCursor(QCursor(Qt.WaitCursor))
        
        i = 0
        curr = None
        for serv in self.server_list:
            self.ui.cmb_servers.addItem("[%s] %s" % (serv['group'], serv['name'], ), userData=serv)
            self.ui.cmb_servers.setItemIcon(i, QtGui.QIcon(ROOT_DIR+'/media/workgroup.png'))
            
            ### Start db_worker for every server ###
            self.start_db_workers('refresh', serv['url'], i, selected_now)
            ### end start db_worker for every server ###
            
            if selected_now and selected_now['url'] == serv['url']:
                self.ui.cmb_servers.setCurrentIndex(i)
                cur = i
            i += 1

        self.connect(self.ui.cmb_servers, QtCore.SIGNAL("currentIndexChanged (int)"), self.on_server_changed)
        self.connect(self.ui.tlw_db_list, QtCore.SIGNAL('list_currentChanged (const QModelIndex &)'), self.db_selection_changed)
        self.connect(self.ui.tlw_view_list, QtCore.SIGNAL('list_currentChanged (const QModelIndex &)'), self.view_selection_changed)
        
        self.connect(self.ui.btn_refresh_all, QtCore.SIGNAL("clicked()"), self.btn_refresh_all_react)
        self.connect(self.ui.btn_ping, QtCore.SIGNAL("clicked()"), self.btn_ping_react)
        
        self.connect(self.ui.btn_clean_views, QtCore.SIGNAL("clicked()"), self.btn_cleanviews_react)
        self.connect(self.ui.btn_compact_db, QtCore.SIGNAL("clicked()"), self.btn_compact_db_react)
        self.connect(self.ui.btn_compact_views, QtCore.SIGNAL("clicked()"), self.btn_compact_views_react)
        self.connect(self.ui.btn_compact, QtCore.SIGNAL("clicked()"), self.btn_compact_react)
        

        self.ui.btn_refresh_all.setIcon(QtGui.QIcon(ROOT_DIR+'/media/refresh.png'))
        
        self.ui.btn_clean_views.setIcon(QtGui.QIcon(ROOT_DIR+'/media/clean.png'))
        self.ui.btn_compact_views.setIcon(QtGui.QIcon(ROOT_DIR+'/media/compact.png'))
        self.ui.btn_compact_db.setIcon(QtGui.QIcon(ROOT_DIR+'/media/compact.png'))
        
        self.ui.btn_compact.setIcon(QtGui.QIcon(ROOT_DIR+'/media/compact.png'))
        self.ui.btn_ping.setIcon(QtGui.QIcon(ROOT_DIR+'/media/ping.png'))
        
        #worker's main timer
        self.timer = QTimer()
        self.connect(self.timer, QtCore.SIGNAL("timeout()"), self.workerTimer_update) 
        self.timer.start(300)
        #db_worker's timer
        self.db_timer = QTimer()
        self.connect(self.db_timer, QtCore.SIGNAL("timeout()"), self.db_timer_update) 
        self.db_timer.start(5000)
            
    
    
    def start_db_workers(self, command, serv_url, index, selected_now):
        if command == 'refresh' or command == 'refresh_all':
            self_db_pipe, remote_db_pipe = multiprocessing.Pipe(duplex = True)
            db_connector = DbWorker(remote_db_pipe, command, serv_url, index, selected_now)
            self.db_workers_list.append({'pipe':self_db_pipe,'thread':db_connector})
            db_connector.start()
        if command == 'db_change':
            self_db_pipe, remote_db_pipe = multiprocessing.Pipe(duplex = True)
            db_connector = DbWorker(remote_db_pipe, command, serv_url, index, selected_now, self.cur_server_dbs)
            self.db_workers_list.append({'pipe':self_db_pipe,'thread':db_connector})
            db_connector.start()
        
    
    def db_timer_update(self):
        for worker_obj in self.db_workers_list:
            worker = worker_obj['pipe']
            while worker.poll():
                data = worker.recv()
                if "error" in data:
                    QMessageBox(QMessageBox.Critical, 'Error', 
                    '''Error while work on command "%s"
                    Server url: "%s"
                    Error: %s''' % (data["command"], data['url'], data['error']), QtGui.QMessageBox.Ok).exec_()   
                elif "command" in data and data["command"] == "end_db_change":
                    view_list = data['view_list']
                    self.cur_server_dbs[data['selected_now'].name] = data['cur_server_dbs'][data['selected_now'].name]
                    self.ui.btn_refresh_all.setEnabled(True)
                    if self.index == data['index']:	
						if self.cur_server_dbs[self.selected_db.name]["last_refresh"] == "Unknown":
							self.ui.lbl_last_update.setText("Unknown")
						else:
							self.ui.lbl_last_update.setText(self.cur_server_dbs[self.selected_db.name]["last_refresh"].strftime(DATETIME_FMT))
						self.view_model = DBViewModel(view_list)
						self.ui.tlw_view_list.setModel(self.view_model)
						self.ui.tlw_view_list.setEnabled(True)
						self.ui.btn_clean_views.setEnabled(True)
						self.ui.btn_compact_db.setEnabled(True)
						self.ui.btn_compact_views.setEnabled(True)
                    for i in range(self.view_model.columnCount()):
                        self.ui.tlw_view_list.resizeColumnToContents(i)
                    self.unsetCursor() 
                elif 'server_url' and 'db_names' and 'cur_server_dbs' in data:
                    self.serv_db_list.append({ 'server':data['server_url'], "db_names":data['db_names'], 'cur_server_dbs':data['cur_server_dbs'] })
                    if "command" in data and data["command"] == "end_refresh": #or data["command"] == "end_refresh_all":
                        if data["selected_now"]["url"] == data["server_url"]:
                            self.cur_server_dbs = data["cur_server_dbs"]
                            if self.index == -1:
                                self.on_server_changed(data["index"])
                            self.ui.tlw_db_list.setEnabled(True)
                            self.ui.btn_clean_views.setEnabled(False)
                            self.ui.btn_compact.setEnabled(False)
                            self.ui.btn_compact_db.setEnabled(False)
                            self.ui.btn_compact_views.setEnabled(False)
                            self.ui.btn_ping.setEnabled(False)
                            self.ui.btn_refresh_all.setEnabled(True)
                    if self.index == data['index'] and data["command"] == "end_refresh_all":
                        self.db_model = DBListModel(data['cur_server_dbs'], data['db_names'])        
                        self.ui.tlw_db_list.setModel(self.db_model)
                        self.ui.tlw_db_list.setEnabled(True)
                        tlw_db_list_sel_model = self.ui.tlw_db_list.selectionModel()
                        i = 0
                        while i < self.ui.tlw_db_list.model().rowCount():
                            if self.selected_db.name and self.ui.tlw_db_list.model().index(i,0).data() == self.selected_db.name:
                                j = 0
                                while j < self.ui.tlw_db_list.model().columnCount():
                                    tlw_db_list_sel_model.select(self.ui.tlw_db_list.model().index(i,j),QItemSelectionModel.Select)
                                    j += 1
                            i += 1
                        try:
                            cur_timestamp = datetime.now()
                            self.cur_server_dbs[self.selected_db.name]['last_refresh'] = cur_timestamp
        
                            info = self.selected_server[self.selected_db.name].info()
                            self.cur_server_dbs[self.selected_db.name]["size"] = info['disk_size']
                            self.cur_server_dbs[self.selected_db.name]["docs"] = info['doc_count']
        
                            self.ui.lbl_last_update.setText(cur_timestamp.strftime(DATETIME_FMT))
                            for row in self.view_model.view_list:
                                self.start_view_worker("get_info", {"row_id": row['id']})
                                row["refreshing"] = "now"
                            self.view_model.update_data()
                            self.db_model.update_data()
                        except:
                            logging.debug('DB Manager: no database found on refresh or you dont have permisions')
                            self.view_model.view_list = []
                            self.view_model.update_data()
                        self.ui.tlw_view_list.setEnabled(True)
                        self.unsetCursor()
                    if self.index != -1 and self.index != data['index']:
                        self.on_server_changed(self.index)
                        
    
    def on_server_changed(self, index):
        """Slot for signal "currentIndexChanged" of servers combobox
        
            Clear old data and create and populate database list of selected server
        """
        self.index = index
        self.server = self.server_list[index]
        self.setWindowTitle("%s - %s"%(self.win_name, self.server['name']))
        if self.server_view_list.get(self.server['url']) is None:
            self.server_view_list[self.server['url']] = {}
        
        try:
            self.selected_server = Server(str(self.server['url']))
        except:
            self.selected_server = None
        for server in self.serv_db_list:
            if server['server'] == self.server['url']:
                self.server_view_list[self.server['url']] = server["cur_server_dbs"]
                self.cur_server_dbs = self.server_view_list[self.server['url']]
                self.db_model = DBListModel(server['cur_server_dbs'], server['db_names'])        
                self.ui.tlw_db_list.setModel(self.db_model)
                self.db_model.update_data()
                self.view_model = DBViewModel([])
                self.ui.tlw_view_list.setModel(self.view_model)
                for i in range(self.db_model.columnCount()):
                    self.ui.tlw_db_list.resizeColumnToContents(i)
        self.unsetCursor()
        
    def db_selection_changed(self, index):
        """Slot for signal "list_currentChanged" of database tree view list
            Clear old view list and populate it with new data from selected database
        """
        self.setCursor(QCursor(Qt.WaitCursor))
        self.selected_db = self.selected_server[self.db_model.db_list[index.row()]]
        win_name = "%s - %s - %s"%(self.win_name, self.server['name'], self.selected_db.name)
        self.setWindowTitle(win_name)
        self.ui.tlw_view_list.setEnabled(False)
        self.start_db_workers('db_change', self.server['url'], self.index, self.selected_db)
        
    def view_selection_changed(self):
        """Slot for signal "list_currentChanged" of view tree view list
   
            Enable control buttons to operate with view
        """
        self.ui.btn_ping.setEnabled(True)
        self.ui.btn_compact.setEnabled(True)
        
        
    def btn_refresh_all_react(self):
        """Slot for signal "clicked()" of "Refresh all" button
        
            Create worker for each view of selected database and send signal for update information about it
        """
        self.setCursor(QCursor(Qt.WaitCursor))
        self.start_db_workers('refresh_all', self.server['url'], self.index, self.selected_server)
        self.ui.tlw_view_list.setEnabled(False)
        self.ui.tlw_db_list.setEnabled(False)
        self.ui.btn_ping.setEnabled(False)
        self.ui.btn_compact.setEnabled(False)
        
    def btn_ping_react(self):
        """Slot for signal "clicked()" of "Ping" button
        
            Create worker for selected view of selected database and send signal to rebuild it
        """
        name = self.view_model.data(self.ui.tlw_view_list.currentIndex(), VIEW_INFO_ROLE)['name']
        self.start_view_worker("ping", {"view_name":name})
    
    def btn_cleanviews_react(self):
        """Slot for signal "clicked()" of "Cleanup views" button
        
            Send signal to cleanup views on selected database
        """
        self.start_view_worker("cleanup_views")
        
    def btn_compact_db_react(self):
        """Slot for signal "clicked()" of "Compact db" button
        
            Send signal to compact selected database
        """
        self.start_view_worker("compact_db")
    
    def btn_compact_views_react(self):
        """Slot for signal "clicked()" of "Compact views" button
        
           Send signal to compact each views in selected database
        """
        self.start_view_worker("compact_views")
    
    def btn_compact_react(self):
        """Slot for signal "clicked()" of "Compact" button
        
            Send signal to compact selected views in selected database
        """
        name = self.view_model.data(self.ui.tlw_view_list.currentIndex(), VIEW_INFO_ROLE)['name']
        self.start_view_worker("compact_view", {"view_name":name})
    
    def start_view_worker(self,command,params=None):
        """Multifunctional structure (function) 
            
            Implement functionality of control buttons:
                Ping
                Compact
                Cleanup views
                Compact db
                Compact views
        """       
        if command == 'get_info' or command == "ping":
            self_pipe, remote_pipe = multiprocessing.Pipe(duplex = True)
            connector = ViewWorker(remote_pipe, self.server['url'], command, self.selected_db.name, params)
            self.view_workers_list.append({'pipe':self_pipe,'thread':connector})
            connector.start()
        elif command == "cleanup_views":
            try:
                result = self.selected_db.view_cleanup()
                if result:
                    QMessageBox(QMessageBox.Information, 'Information', 
'''"Cleanup Views" was initiated successfully.
Server url: "%s"
Database name: "%s"
Date: %s''' % (self.server['url'], self.selected_db.name, datetime.now().strftime(DATETIME_FMT),), QtGui.QMessageBox.Ok).exec_() 
                else:
                    self.show_error(command, params, "Error status was returned by the wrapper")  
            except:
                self.show_error(command, params, sys.exc_info()[1])
        
        elif command == "compact_db" :
            try:
                self.selected_db.compact()
                QMessageBox(QMessageBox.Information, 'Information', 
'''"Compact Database" was initiated successfully.
Server url: "%s"
Database name: "%s"
Date: %s''' % (self.server['url'], self.selected_db.name, datetime.now().strftime(DATETIME_FMT),), QtGui.QMessageBox.Ok).exec_()             
            except:
                self.show_error(command, params, sys.exc_info()[1]) 
        
        elif command == "compact_views":
            result_arr = []
            try:
                for view in self.view_model.view_list:
                    result = self.selected_db.compact_view(view["name"])
                    #print "%s: %s" % (view["name"], (lambda:"Yes", lambda:"No")[result](),)
                    result_arr.append("%s: %s" % (view["name"], {True: "Yes", False: "No"}[result],))
                report = "\n".join(["%s" % d for d in result_arr])
                QMessageBox(QMessageBox.Information, 'Information', 
'''"Compact Views" was initiated successfully.
Server url: "%s"
Database name: "%s"
Date: %s
Report: %s''' % (self.server['url'], self.selected_db.name, datetime.now().strftime(DATETIME_FMT), report,), QtGui.QMessageBox.Ok).exec_()                     
            except:
                self.show_error(command, params, sys.exc_info()[1])
        elif command == "compact_view":
            try:
                result = self.selected_db.compact_view(params["view_name"])
                report = "%s: %s" % (params["view_name"], {True: "Yes", False: "No"}[result],)
                QMessageBox(QMessageBox.Information, 'Information', 
'''"Compact View" was initiated successfully.
Server url: "%s"
Database name: "%s"
View name: %s
Date: %s
Report: %s''' % (self.server['url'], self.selected_db.name, params["view_name"], datetime.now().strftime(DATETIME_FMT), report,), QtGui.QMessageBox.Ok).exec_()                     
            except:
                self.show_error(command, params, sys.exc_info()[1])
                
    def show_error(self,command, params, error):
        """Show messageBox with information about error in db functionality 
        """
        QMessageBox(QMessageBox.Critical, 'Error', 
'''Error while work on command "%s"
Server url: "%s"
Database name: "%s"
Parameters: %s
Date: %s
Error: %s''' % (command, self.server['url'], self.selected_db.name, params,datetime.now().strftime(DATETIME_FMT), error), QtGui.QMessageBox.Ok).exec_()        
    
    def disabling_refresh(self):
        """Disable refresh button 
        """
        self.ui.btn_refresh_all.setEnabled(False)
        self.ui.lbl_last_update.setText("Unknown")
        
    def workerTimer_update(self):
        """Main worker loop 
        """
        remove_ready = []
        i = 0
        flag_was_changes = False
        for worker_obj in self.view_workers_list:
            worker = worker_obj['pipe']
            while worker.poll():
                data = worker.recv()
                if "error" in data:
                    QMessageBox(QMessageBox.Critical, 'Error', 
'''Error while work on command "%s"
Server url: "%s"
Database name: "%s"
Parameters: %s
Date: %s
Error: %s''' % (data["command"], data['url'], data['db_name'], data["params"], data["updated"], data["error"],), QtGui.QMessageBox.Ok).exec_()
                    remove_ready.append(worker_obj)
                    flag_was_changes = True   
                else:
                    if "command" in data:
                        if data["command"] == "get_info":
                            serv = self.server_view_list[data['url']]
                            db_heandler = serv[data['db_name']]
                            row_heandler = db_heandler[data['params']["row_id"]]
                            result_heandler = data['result']
                            row_heandler['view_index'] = result_heandler['view_index']
                            row_heandler["refreshing"] = "ready"
                            remove_ready.append(worker_obj)
                            flag_was_changes = True
                            

                            
                            
                        elif data["command"] == "ping":
                            QMessageBox(QMessageBox.Information, 'Information', 
'''Ping complete successfully.
Server url: "%s"
Database name: "%s"
View name: "%s"
Done on: %s''' % (data['url'], data['db_name'], data["params"]["view_name"], data["updated"],), QtGui.QMessageBox.Ok).exec_()
                            remove_ready.append(worker_obj)
                            flag_was_changes = True   
                i += 1
        
        
        for worker in remove_ready:
            self.view_workers_list.remove(worker)
        
        if flag_was_changes:
            self.view_model.update_data()
            for i in range(self.view_model.columnCount()):
                self.ui.tlw_view_list.resizeColumnToContents(i) 
            
    
    def closeEvent(self,event):
        try:
            self.mainWindow.dbmanager_windows.remove(self)
        except:
            #print "error removing from db manager windows list"
             logging.debug('ReplicationWindow: error removing from db manager windows list')
        
