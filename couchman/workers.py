import sys, multiprocessing, logging
from time import sleep,time
from datetime import datetime, timedelta
from couchdbcurl import Server
from config import DATETIME_FMT

class ServerWorker(multiprocessing.Process):
    
    def __init__(self,pipe,server, default):
        multiprocessing.Process.__init__(self)
        self.tries = 0
        self.pipe = pipe
        self.server = server
        self.flag = True
        self.address = server['url']
        self.db_server = Server(str(self.address))
        try:
            self.update_period = float(server.get('autoupdate'))
        except:
            self.update_period = float(default['autoupdate'])
        
        self.last_update = time()
    
    def update(self):
        #logging.debug("worker: update command for %s" % self.address)
        if self.server['enabled']:
            try:
                tasks = self.db_server.tasks()
                error = " "
            except:
                tasks = None
                error = sys.exc_value
            try:
                ver = "ver. %s" % self.db_server.version
                status = True
                self.tries = 0
            except:
                ver = "-"
                status = False
                self.tries += 1 
            try:
                persistent = self.db_server['_replicator']['_all_docs']
            except:
                persistent = None
        else:
            ver = "-"
            tasks = None
            persistent = None
            status = False
        self.last_update = time()
        if self.tries:
            update = datetime.now() - timedelta(seconds = self.update_period * self.tries)
        else:
            update = datetime.now()
        self.pipe.send({"command": "end_update_server", 
                        "url": self.server['url'],
                        "data":{"enabled": self.server['enabled'],
                                "updated": update,
                                "version": ver,
                                "status": status,
                                "tasks": tasks,
                                "error": error,
                                "persistent":persistent}})
        
    def run(self):
        while self.flag:
            while self.pipe.poll():
                data = self.pipe.recv()
                if "command" in data:
                    command = data['command']
                    if command == "update_server":
                        self.update()
                    elif command == "update_data":
                        self.server = data['data']
                        self.address = self.server['url']
                        self.db_server = Server(str(self.address))
                        try:
                            self.update_period = float(self.server.get('autoupdate'))
                        except:
                            self.update_period = None
                        
                    elif command == "shutdown":
                        logging.debug("worker: shutdown command for %s" % self.address)
                        self.flag = False
                        
                        return
            sleep(0.05)
            
            if self.update_period and time() > self.last_update + self.update_period and self.server['enabled']:
                self.update()
                
                

class ReplicatorWorker(multiprocessing.Process):
    def __init__(self,pipe,url):
        multiprocessing.Process.__init__(self)
        self.pipe = pipe
        self.url = url
        self.db_server = Server(str(url))
        self.docs_info = []
        
    def run(self):
        while True:
            while self.pipe.poll():
                data = self.pipe.recv()
                if "command" in data:
                    command = data['command']
                    if command == "get_replicator_docs":
                        try:
                            persistent = self.db_server['_replicator']['_all_docs']
                        except:
                            persistent = None
                            logging.debug("replicator worker error: %s" % sys.exc_info()[1])
                        if persistent:
                            for doc in persistent["rows"]: 
                                if not doc["id"].startswith('_design/'):
                                    self.docs_info.append({"id":doc["id"], "info":persistent['_db'][doc["id"]]})
                                    if not "source" in persistent['_db'][doc["id"]]: 
                                        print 'There is no source in %s. Doc ID: %s' % (persistent['_db'].name, persistent['_db'][doc["id"]]["_id"])
                            self.pipe.send({"command": "end_get_replicator_docs", 
                                            "data":{"url": self.url,
                                                    "docs":self.docs_info}})
                        else:
                            self.pipe.send({"command": "end_get_replicator_docs", 
                                            "data":{"url": self.url,
                                                    "docs": None}})
                        self.docs_info = []
            sleep(0.5)

class ReplicationWorker(multiprocessing.Process):
    
    def __init__(self,pipe,data):
        multiprocessing.Process.__init__(self)
        self.pipe = pipe
        self.source = data.get('source')
        self.target = data.get('target')
        self.filter = data.get('filter',"")

        self.query = data.get('query', "")
        self.continuous = data.get('continuous')
        self.proxy = data.get('proxy', "")
        self.flag = True
        server = data.get('server')
        self.server_address = server.get('url')
        self.db_server = Server(str(self.server_address))
        self.flag = True
        
        
    def run(self):

        logging.debug("replication worker: run replication worker for %s" % self.server_address)
        while self.flag:
            while self.pipe.poll():
                data = self.pipe.recv()
                if "command" in data:
                    command = data['command']
                    if command == "start_replication":
                        error = None
                        args = {}
                        if self.proxy:
                            args['proxy'] = self.proxy
                        if self.filter:
                            args['filter'] = self.filter
                            if self.query:
                                args['query_params'] = self.query
                        if self.continuous:
                            print "replicate url: source: %s, target: %s, continuous: true, args: %s" % (self.source, self.target, args,)
                            try:
                                self.db_server.replicate(self.source, self.target, continuous=True, **args)
                            except:
                                logging.debug("worker: replication creation error for %s" % self.server_address)
                                error = sys.exc_info()[1]
                        else:
                            print "replicate url: source: %s, target: %s, continuous: false, args: %s" % (self.source, self.target, args,)
                            try:
                                self.db_server.replicate(self.source, self.target, **args)
                            except:
                                logging.debug("worker: replication creation error for %s" % self.server_address)
                                error = sys.exc_info()[1]
                            
                        if error:
                            self.pipe.send({
                                "command":'error',
                                "url": self.server_address,
                                "error": error,
                                "source": self.source,
                                "target": self.target,
                                "filter": self.filter,
                                "query": self.query,
                                "proxy": self.proxy,
                                "continuous": self.continuous,
                            })
                        else:
                            self.pipe.send({
                                "command": "done",
                                "message": "Replication start successfully. Details:",
                                "url": self.server_address,
                                "source": self.source,
                                "target": self.target,
                                "filter": self.filter,
                                "query": self.query,
                                "proxy": self.proxy,
                                "continuous": self.continuous,
                            })
                        self.flag = False
                    elif command == "stop_replication":
                        error = None
                        try:
                            self.db_server.replicate(self.source, self.target,continuous=True, cancel = True)
                            self.continuous = True
                        except:
                            try:
                                self.db_server.replicate(self.source, self.target, cancel = True)
                                self.continuous = False
                            except:
                                error = sys.exc_info()[1]
                        if error:
                            self.pipe.send({
                                "command": 'error',
                                "url": self.server_address,
                                "error": error,
                                "source": self.source,
                                "target": self.source,
                                "filter": self.filter,
                                "query": self.query,
                                "proxy": self.proxy,
                                "continuous": self.continuous,
                            })
                        else:
                            self.pipe.send({
                                "command": "done",
                                "message": "Replication stop successfully. Details:",
                                "url": self.server_address,
                                "source": self.source,
                                "target": self.target,
                                "filter": self.filter,
                                "query": self.query,
                                "proxy": self.proxy,
                                "continuous": self.continuous,
                            })
                        self.flag = False       
                               
                    if command == "shutdown":
                        logging.debug("worker: shutdown command for %s" % self.server_address)
                        self.flag = False
                        
                        return      
            sleep(0.5)
            
class ViewWorker(multiprocessing.Process):
    
    def __init__(self,pipe,url,command,db_name,params):
        multiprocessing.Process.__init__(self)
        self.pipe = pipe
        self.params = params
        self.command = command
        self.address = url
        self.db_server = Server(str(self.address))
        self.db = self.db_server[db_name]
        
    
    def send_error(self, error):
        self.pipe.send({"command":self.command,
                        "url": self.address,
                        "updated": datetime.now(),
                        "db_name": self.db.name,
                        "params": self.params,
                        "error": error,
                        })
    
    def send_result(self, result):
        self.pipe.send({"command":self.command,
                        "url": self.address,
                        "updated": datetime.now(),
                        "db_name": self.db.name,
                        "params": self.params,
                        "result": result,
                        })
    
    def run(self):
        if self.command == "get_info":
            try:
                result = self.db.design_info(str(self.params["row_id"]))
                self.send_result(result)
            except:
                self.send_error(sys.exc_info()[1])
        elif self.command == "ping":
            try:
                doc_name = self.db['_design/' + self.params["view_name"]].views.keys()[0]
                self.db.view(self.params["view_name"] + '/' + doc_name, limit=0, stale='update_after').rows
                self.send_result("")
            except:
                self.send_error(sys.exc_info()[1])



class DbWorker(multiprocessing.Process):
    
    def __init__(self, pipe, command, server, serv_index, selected = None, cur_server_dbs = None):
        multiprocessing.Process.__init__(self)
        self.pipe = pipe
        self.command = command
        self.server_url = server
        self.selected_now = selected
        self.serv_index = serv_index
        try:
            self.db_server = Server(str(server))
            self.error = None
        except:
            self.db_server = None
            self.error = sys.exc_info()[1]
        if cur_server_dbs:
            self.cur_server_dbs = cur_server_dbs
        else:
            self.cur_server_dbs = {}
        self.db_names = []
        
    
    def send_error(self, error):
        self.pipe.send({"command":self.command,
                       "url": self.db_server,
                       "error": error,
                       })
    
    def run(self):
        if self.error:
            self.send_error(self.error)
        elif self.command == "refresh" and self.db_server or self.command == "refresh_all":
            for db in self.db_server:
                if self.cur_server_dbs.get(db) is None:
                    try:
                        info = self.db_server[db].info()
                        self.cur_server_dbs[db] = {"connect":True,"last_refresh":"Unknown", "name":db, "size":info['disk_size'], "docs":info['doc_count']}
                    except:
                        self.cur_server_dbs[db] = {"connect":False,"last_refresh":"Unknown", "name":db, "size":"-", "docs":"-"}
                else:
                    try:
                        info = self.db_server[db].info()
                        self.cur_server_dbs[db]["connect"] = True
                        self.cur_server_dbs[db]["size"] = info['disk_size']
                        self.cur_server_dbs[db]["docs"] = info['doc_count']
                    except:
                        self.cur_server_dbs[db]["connect"] = False
                        self.cur_server_dbs[db]["size"] = "-"
                        self.cur_server_dbs[db]["docs"] = "-"
                self.db_names.append(db)
                self.db_names.sort()
            self.pipe.send({'command':'end_%s' % (self.command),
                            'db_names':self.db_names,
                            'cur_server_dbs':self.cur_server_dbs,
                            'server_url': self.server_url,
                            'selected_now':self.selected_now,
                            'server': self.db_server,
                            'index': self.serv_index,
                            })
        elif self.command == "db_change":
            view_list = []
            try:
                row_list = self.selected_now.view('_all_docs', startkey = "_design/", endkey = "_design0").rows
                for row in row_list:
                    name = row.key[8:]
                    if self.cur_server_dbs[self.selected_now.name].get(row.id) is None:
                        self.cur_server_dbs[self.selected_now.name][row.id] = {"name":name, "revision":row.value['rev'], "id": row.id}
                    view_list.append(self.cur_server_dbs[self.selected_now.name][row.id])
                self.pipe.send({'command':'end_db_change',
                                'view_list':view_list,
                                'selected_now':self.selected_now,
                                'cur_server_dbs':self.cur_server_dbs,
                                'index':self.serv_index,
                                })
            except: 
                print sys.exc_info()[1]
                self.send_error(sys.exc_info()[1])
                logging.debug('DB Manager: no database found on db selection changed or you dont have permisions')
