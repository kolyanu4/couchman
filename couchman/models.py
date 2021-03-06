import logging, urlparse
from datetime import datetime, timedelta
from PySide import QtGui, QtCore
from operator import itemgetter
from config import *

class ServerTreeModel(QtCore.QAbstractTableModel):
    def __init__(self, mainWindow,parent = None):
        super(ServerTreeModel, self).__init__(parent)
        self.servers = []
        self.headers = (" ", "Name", "Group", "Info")
        self.mainWindow = mainWindow
        self.enabled_brush = QtGui.QBrush()
        self.enabled_brush.setColor(QtGui.QColor(0,200,0))
        
        self.disabled_brush = QtGui.QBrush()
        self.disabled_brush.setColor(QtCore.Qt.gray)
        

    def columnCount(self, parent=None):
        return len(self.headers)
        
    def rowCount(self, parent=QtCore.QModelIndex()):
        return len(self.servers)
    
    
    def data(self, index, role):
        if not index.isValid():
            return None
        if role == QtCore.Qt.DisplayRole:
            if index.column() == 1:
                return self.servers[index.row()].get('name')
            elif index.column() == 2:
                return self.servers[index.row()].get('group')
            elif index.column() == 3:
                return self.servers[index.row()].get('version')
    
        elif role == QtCore.Qt.ForegroundRole:
            if self.servers[index.row()].get('enabled'):
                return self.enabled_brush
            else:
                return self.disabled_brush
        elif role == SERVER_INFO_ROLE:
            return self.servers[index.row()]
        elif role == QtCore.Qt.DecorationRole:
            if index.column() == 0:
                obj = self.servers[index.row()]
                last = obj.get('last_update')
                flag_enabled = obj.get('enabled')
                if last:
                    delta = datetime.now() - last
                    dif = delta.seconds
                else:
                    dif = INFINITY
                str_autoupdate = self.servers[index.row()].get('autoupdate')
                if str_autoupdate:
                    period = float(str_autoupdate)
                else:
                    period = -1.0
                    
                if period < 0 or not flag_enabled:
                    return QtGui.QIcon(ROOT_DIR+'/media/circle_blue.png')
                elif dif > 6 * period:
                    return QtGui.QIcon(ROOT_DIR+'/media/circle_red.png')
                elif dif > 3 * period:
                    return QtGui.QIcon(ROOT_DIR+'/media/circle_orange.png')
                else:
                    return QtGui.QIcon(ROOT_DIR+'/media/circle_green.png')
            
        return None
    
    
    def headerData(self, column, orientation, role):
        if (orientation == QtCore.Qt.Horizontal and role == QtCore.Qt.DisplayRole):
            try:
                return self.headers[column]
            except IndexError:
                pass

        return None
    
    def getServByAddress(self,address):
        for serv in self.servers:
            if serv['url'] == address:
                return serv
        return None

    def removeServRecord(self,serv_obj):
        try:
            self.servers.remove(serv_obj)
            logging.debug("ServerModel: remove record complete")
            self.update_data()
        except:
            logging.debug("ServerModel: remove record error")
        
    def update_data(self):
        self.sort(1,QtCore.Qt.AscendingOrder)
        self.emit(QtCore.SIGNAL('layoutChanged()'))
        self.emit(QtCore.SIGNAL('dataChanged(const QModelIndex &, const QModelIndex &)'), self.index(0,0), self.index(self.rowCount(),self.columnCount()))
        
        
    def sort(self, Ncol, order):
        self.servers.sort(cmp=self.cmp_func, reverse=order)
        #self.update_data()

    def cmp_func(self,a,b):

        if a['group'] == b['group']:
            return cmp(a['name'], b['name'])
        else:
            return cmp(a['group'], b['group'])


class TaskTreeModel(QtCore.QAbstractTableModel):
    def __init__(self, serv_obj,parent = None):
        super(TaskTreeModel, self).__init__(parent)
        self.tasks_rendered = []
        self.runetime = []
        self.need_rendering = True
        self.server_list = serv_obj['replications']

        self.server_obj = serv_obj
        self.headers = ("Type", "Object", "Progress", "Pid", "Started on", "Updated on")
        self.active_brush = QtGui.QBrush()
        self.active_brush.setColor(QtGui.QColor(0,200,0))
        
        self.nonactive_brush = QtGui.QBrush()
        self.nonactive_brush.setColor(QtCore.Qt.red)

    def columnCount(self, parent=None):
            return len(self.headers)
        
    def rowCount(self, parent=QtCore.QModelIndex()):
        if self.need_rendering:
            self.render()
        return len(self.tasks_rendered)
    
    
    def data(self, index, role):
        if not index.isValid() or index.row() < 0:
            return None
        if self.need_rendering:
            self.render()
        if role == QtCore.Qt.DisplayRole or role == QtCore.Qt.ToolTipRole:
            if index.column() == 0:
                if self.tasks_rendered[index.row()].get('record_type') != 2:
                    return self.tasks_rendered[index.row()].get('type')
                else:
                    return "replication"
            if index.column() == 1:
                if self.tasks_rendered[index.row()].get('type') == 'replication':
                    return '%s -> %s (%s/%s)' % (self.tasks_rendered[index.row()].get('source'), self.tasks_rendered[index.row()].get('target'), format(self.tasks_rendered[index.row()].get('checkpointed_source_seq'), ',d'), format(self.tasks_rendered[index.row()].get('source_seq'), ',d'))
                elif self.tasks_rendered[index.row()].get('type') == 'view_compaction':
                    return '%s@%s' % (self.tasks_rendered[index.row()].get('design_document'), self.tasks_rendered[index.row()].get('database'))
                elif self.tasks_rendered[index.row()].get('type') == 'indexer':
                    return '%s@%s (%s/%s)' % (self.tasks_rendered[index.row()].get('design_document'), self.tasks_rendered[index.row()].get('database'), format(self.tasks_rendered[index.row()].get('changes_done'), ',d'), format(self.tasks_rendered[index.row()].get('total_changes'), ',d'))
                elif self.tasks_rendered[index.row()].get('type') == 'database_compaction':
                    return '%s (%s/%s)' % (self.tasks_rendered[index.row()].get('database'), format(self.tasks_rendered[index.row()].get('changes_done'), ',d'), format(self.tasks_rendered[index.row()].get('total_changes'), ',d'))
                else:
                    return self.tasks_rendered[index.row()].get('task')
            if index.column() == 2:
                if self.tasks_rendered[index.row()].get('record_type') != 2:
                    if 'progress' in self.tasks_rendered[index.row()]:
                        return "%s%s" % (self.tasks_rendered[index.row()].get('progress'), '%')
                    else:
                        return self.tasks_rendered[index.row()].get('status')
                else:
                    return None
            if index.column() == 3:
                if self.tasks_rendered[index.row()].get('record_type') != 2:
                    return self.tasks_rendered[index.row()].get('pid')
                else:
                    return None
            if index.column() == 4:
                if 'started_on' in self.tasks_rendered[index.row()]:
                    started = datetime.fromtimestamp(self.tasks_rendered[index.row()].get('started_on'))
                    return '%s' % (started)
                else:
                    return None
            if index.column() == 5:
                if 'updated_on' in self.tasks_rendered[index.row()]:
                    updated =datetime.fromtimestamp(self.tasks_rendered[index.row()].get('updated_on'))
                    return '%s' % (updated)
                else:
                    return None

            
        elif role == QtCore.Qt.BackgroundColorRole:
            if index.column() == 2 and self.tasks_rendered[index.row()].get('progress') == 100:
                return QtGui.QColor(26,207,63)
        elif role == QtCore.Qt.ForegroundRole:
            if index.column() == 2 and self.tasks_rendered[index.row()].get('record_type') == 1:
                return self.active_brush
            elif self.tasks_rendered[index.row()].get('record_type') == 2:
                return self.nonactive_brush
            else:
                return QtGui.QBrush()
        elif role == TASK_INFO_ROLE:
            try:
                return self.tasks_rendered[index.row()]
            except:
                return None
        return None
    
    
    def headerData(self, column, orientation, role):
        if (orientation == QtCore.Qt.Horizontal and role == QtCore.Qt.DisplayRole):
            try:
                return self.headers[column]
            except IndexError:
                pass

        return None
    
    def finde(self,source,target):
        for rec in self.tasks_rendered:
            if rec.get('type') == 'replication':
                txt_lst = rec.get('task').split(' ')
                if rec.get('record_type') != 2:
                    task_source = txt_lst[1]
                    task_target = txt_lst[3]
                else:
                    task_source = txt_lst[0]
                    task_target = txt_lst[2]      
                                 
                if task_source == source and task_target == target:
                    return rec
        return None
         
    def update_data(self):
        self.emit(QtCore.SIGNAL('layoutChanged()'))
        self.emit(QtCore.SIGNAL('dataChanged(const QModelIndex &, const QModelIndex &)'), self.index(0,0), self.index(self.rowCount(),self.columnCount()))
            
        #self.reset()
       
                   
        
    def update_runetime(self,runetime_list):
        if runetime_list is not None:
            self.runetime = runetime_list
        else:
            self.runetime = []
        self.need_rendering = True
        self.update_data()
    
    def render(self):
        self.tasks_rendered = []
        for task in self.runetime:
            task['record_type'] = 0
            self.tasks_rendered.append(task)
            
        nonactive = []
  
        for rec in self.server_list:
            isNonActive = True
            for task in self.tasks_rendered:
                if task.get('type') == 'Replication':
                    txt_lst = task.get('task').split(' ')
                    task_source = txt_lst[1]
                    task_target = txt_lst[3]
                    
                    if rec['source'] == task_source and rec['target'] == task_target:
                        task['record_type'] = 1
                        isNonActive = False
            if isNonActive:
                nonactive.append(rec)
        
        for rec in nonactive:
            msg = "%s -> %s" % (rec['source'], rec['target'])
            self.tasks_rendered.append({'task': msg,'record_type': 2, 'proxy': rec.get('proxy',""), 'filter': rec.get('filter', ""), 'query': rec.get('query',"")})
        
        self.need_rendering = False
        self.update_data()


class PersistentTreeModel(QtCore.QAbstractTableModel):
    def __init__(self, replicator = None, parent = None):
        super(PersistentTreeModel, self).__init__(parent)
        if replicator:
            self.replicator = replicator
        else: 
            self.replicator = None
        self.headers = ("ID", "State", "Time", "Source", "Target", "Continuous", "Owner", "User Context")

    def data(self, index, role):
        if not self.replicator: 
            return None
        if not index.isValid() or index.row() < 0:
            return None
        if role == QtCore.Qt.DisplayRole or role == QtCore.Qt.ToolTipRole:
            if index.column() == 0 and "id" in self.replicator[index.row()]:
                return self.replicator[index.row()]["id"]
            if index.column() == 1 and "_replication_state" in self.replicator[index.row()]["info"]:
                return self.replicator[index.row()]["info"]["_replication_state"]
            if index.column() == 2 and "_replication_state_time" in self.replicator[index.row()]["info"]:
                return str(self.to_date(str(self.replicator[index.row()]["info"]["_replication_state_time"])))
            if index.column() == 3:
                return self.addr(self.replicator[index.row()]["info"]["source"])
            if index.column() == 4 :
                return self.addr(self.replicator[index.row()]["info"]["target"])
            if index.column() == 5:
                if 'continuous' in self.replicator[index.row()]["info"] and self.replicator[index.row()]["info"]["continuous"]:
                    return '+'
                else:
                    return '-'
            if index.column() == 6 and "owner" in self.replicator[index.row()]["info"]:
                return self.replicator[index.row()]["info"]["owner"]
            if index.column() == 7:
                if 'user_ctx' in self.replicator[index.row()]["info"]:
                    return str(self.replicator[index.row()]["info"]["user_ctx"])
        elif role == QtCore.Qt.BackgroundColorRole:
            if index.column() == 1 and "_replication_state" in self.replicator[index.row()]["info"] and self.replicator[index.row()]["info"]["_replication_state"] != 'triggered':
                return QtGui.QColor(233,92,92)
            if index.column() == 2:
                if '_replication_state_time' in str(self.replicator[index.row()]["info"]):
                    date = self.to_date(str(self.replicator[index.row()]["info"]["_replication_state_time"]))
                
                    if datetime.now() > date+timedelta(minutes=1):
                        return QtGui.QColor(233,92,92)
                
    def to_date(self, date):
        return datetime.strptime(date.split('+')[0], "%Y-%m-%dT%H:%M:%S")
        

    def addr(self, addr):
        url = urlparse.urlparse(addr)
        if url.username:
            hidden_url = '%(scheme)s://%(username)s:%(password)s@%(hostname)s%(path)s' % {
                'scheme': url.scheme,
                'username': url.username,
                'password': '*' * 8,
                'hostname': url.hostname,
                'path': url.path,
                'query': url.query,
                'fragment': url.fragment,
            }
        elif url.scheme:
            hidden_url = '%(scheme)s://%(hostname)s%(path)s' % {
                'scheme': url.scheme,
                'username': url.username,
                'password': '*' * 8,
                'hostname': url.hostname,
                'path': url.path,
                'query': url.query,
                'fragment': url.fragment,
            }
        else:
            hidden_url = url.path,
        return hidden_url
        
    def rowCount(self, parent=QtCore.QModelIndex()):
        if self.replicator: 
            return len(self.replicator)
        else:
            return 0
    
    def columnCount(self, parent=None):
        return len(self.headers)
    
    def headerData(self, column, orientation, role):
        if (orientation == QtCore.Qt.Horizontal and role == QtCore.Qt.DisplayRole):
            try:
                return self.headers[column]
            except IndexError:
                pass
        return None
        
    def update_data(self):
        self.emit(QtCore.SIGNAL('layoutChanged()'))
        self.emit(QtCore.SIGNAL('dataChanged(const QModelIndex &, const QModelIndex &)'), self.index(0,0), self.index(self.rowCount(),self.columnCount()))
        
        
class DBListModel(QtCore.QAbstractTableModel):
    def __init__(self, server_dbs, db_list,parent = None):
        super(DBListModel, self).__init__(parent)
        self.db_list = []#{'names':[], 'sizes':[], 'docs':[]} 
        self.server_dbs = {}
        self.headers = ("Database", "Size", "Documents",)
        if server_dbs:
            self.server_dbs = server_dbs
        if db_list:
            self.db_list = db_list       

    def rowCount(self, parent=QtCore.QModelIndex()):
        return len(self.db_list)
    
    def columnCount(self, parent=None):
            return len(self.headers)
    
    
    def headerData(self, column, orientation, role):
        if (orientation == QtCore.Qt.Horizontal and role == QtCore.Qt.DisplayRole):
            try:
                return self.headers[column]
            except IndexError:
                pass
        return None
    
    def data(self, index, role):
        if not index.isValid():
            return None
        name = self.db_list[index.row()]
        if role == QtCore.Qt.DisplayRole:
            if index.column() == 0:
                return self.db_list[index.row()]
            elif index.column() == 1:
                size_byte = self.server_dbs[name]["size"]
                return self.splitthousands(str(size_byte))
            elif index.column() == 2:
                return self.splitthousands(str(self.server_dbs[name]["docs"]))

        elif role == QtCore.Qt.DecorationRole:
            if index.column() == 0:
                connect = self.server_dbs[name]["connect"]
                if not connect:
                    return QtGui.QIcon(ROOT_DIR+'/media/circle_red.png')
                return QtGui.QIcon(ROOT_DIR+'/media/database.png')
            
        elif role == QtCore.Qt.TextAlignmentRole:
            if index.column() !=0:
                return QtCore.Qt.AlignRight
        return None
    
    def splitthousands(self,s, sep=','):  
        if len(s) <= 3: return s  
        return self.splitthousands(s[:-3], sep) + sep + s[-3:]
    
    def update_data(self):
        self.emit(QtCore.SIGNAL('layoutChanged()'))
        self.emit(QtCore.SIGNAL('dataChanged(const QModelIndex &, const QModelIndex &)'), self.index(0,0), self.index(self.rowCount(),self.columnCount()))

class DBViewModel(QtCore.QAbstractTableModel):
    def __init__(self, view_list,parent = None):
        super(DBViewModel, self).__init__(parent)
        self.view_list = [] 
        self.headers = (" ", "Name", "Revision","Signature", "Size", "Language", "Clients", "Update", "P.S.", "C.R.", "W.C.", "U.R.", )
        self.colum_tips = ("Status", "View name", "Revision of View", "Signature of View", "Size on disk in MB", "Programming language of View",
                           "Waiting clients", "Update sequence", "Purge sequence", "Is compact running (+ equals True, - equals False)",
                           "Is waiting commit (+ equals True, - equals False)", "Is updater running (+ equals True, - equals False)",  )
        if view_list:
            self.view_list = view_list       

    def rowCount(self, parent=QtCore.QModelIndex()):
        return len(self.view_list)
    
    def columnCount(self, parent=None):
            return len(self.headers)
    
    
    def headerData(self, column, orientation, role):
        if orientation == QtCore.Qt.Horizontal:
            if role == QtCore.Qt.DisplayRole:
                try:
                    return self.headers[column]
                except IndexError:
                    pass
            elif role == QtCore.Qt.ToolTipRole:
                try:
                    return self.colum_tips[column]
                except IndexError:
                    pass
                

        return None
    
    def data(self, index, role):
        if not index.isValid():
            return None
        if role == QtCore.Qt.DisplayRole:
            if index.column() == 1:
                return self.view_list[index.row()].get('name')
            elif index.column() == 2:
                return self.view_list[index.row()].get('revision')
            if self.view_list[index.row()].get('view_index'):
                if index.column() == 3:
                    return self.view_list[index.row()].get('view_index').get('signature')
                elif index.column() == 4:
                    size_byte = self.view_list[index.row()].get('view_index').get('disk_size')
                        
                    return self.splitthousands(str(size_byte))
                elif index.column() == 5:
                    return self.view_list[index.row()].get('view_index').get('language')
                elif index.column() == 6:
                    return self.view_list[index.row()].get('view_index').get('waiting_clients')
                elif index.column() == 7:
                    return self.view_list[index.row()].get('view_index').get('update_seq')
                elif index.column() == 8:
                    return self.view_list[index.row()].get('view_index').get('purge_seq')

        
        elif role == QtCore.Qt.DecorationRole:
            if index.column() == 0:
                if self.view_list[index.row()].get('refreshing') and self.view_list[index.row()]['refreshing'] == "now":
                    return QtGui.QIcon(ROOT_DIR+'/media/refresh.png')
                else:
                    return QtGui.QIcon(ROOT_DIR+'/media/true_symbol.png')
            if self.view_list[index.row()].get('view_index'):
                if index.column() == 9:
                    if self.view_list[index.row()].get('view_index').get('compact_running'):
                        return QtGui.QIcon(ROOT_DIR+'/media/true_state.png')
                    else:
                        return QtGui.QIcon(ROOT_DIR+'/media/false_state.png')
                elif index.column() == 10:
                    if self.view_list[index.row()].get('view_index').get('waiting_commit'):
                        return QtGui.QIcon(ROOT_DIR+'/media/true_state.png')
                    else:
                        return QtGui.QIcon(ROOT_DIR+'/media/false_state.png')
                elif index.column() == 11:
                    if self.view_list[index.row()].get('view_index').get('updater_running'):
                        return QtGui.QIcon(ROOT_DIR+'/media/true_state.png')
                    else:
                        return QtGui.QIcon(ROOT_DIR+'/media/false_state.png')          
               
        elif role == VIEW_INFO_ROLE:
            return self.view_list[index.row()]
        
        elif role == QtCore.Qt.TextAlignmentRole:
            if self.view_list[index.row()].get('view_index'):
                if index.column() == 4 or index.column() == 6 or index.column() == 7 or index.column() == 8:
                    return QtCore.Qt.AlignRight
                    
        return None
    
    def splitthousands(self,s, sep=','):  
        if len(s) <= 3: return s  
        return self.splitthousands(s[:-3], sep) + sep + s[-3:]

    def update_data(self):
        self.emit(QtCore.SIGNAL('layoutChanged()'))
        self.emit(QtCore.SIGNAL('dataChanged(const QModelIndex &, const QModelIndex &)'), self.index(0,0), self.index(self.rowCount(),self.columnCount()))
            
    
