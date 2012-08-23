import json, sys, logging
import os.path
from copy import deepcopy
from config import *
import pprint

class MyJson():
    def __init__(self):
        logging.debug('MyJson: init')
        self.MAIN_DB = None;
    
    def getManDB(self):
        return self.MAIN_DB
    
    def readFromDB(self):
        if os.path.isfile(DB_FILE_PATH):
            logging.debug('MyJson: file exist... start reading')
            with open(DB_FILE_PATH, 'r') as f:
                self.MAIN_DB = json.load(f)
        else:
            logging.debug('MyJson: file not found... create new one')
            body = {"defaults": { "autoupdate": 10.0 }, "servers": []}
            
            with open(DB_FILE_PATH, 'w') as f:
                json.dump(body, f, indent=4, separators=(', ', ': '))     
            
            print DB_FILE_PATH
            
            self.MAIN_DB = body
        return self.getManDB()

    def save(self, DB):
        try:
            dump = deepcopy(self.MAIN_DB)
            runtime = dump['servers']
            dump['servers'] = []
            for serv in DB:
                replications = serv['replications']
                server = { "group":serv['group'], 
                           "name":serv['name'], 
                           "url":serv['url'], 
                           "enabled":serv['enabled'], 
                           "autoupdate":serv['autoupdate'], 
                           "proxy":serv['proxy'],
                           "replications":replications}
                dump['servers'].append(server)
            
            with open(DB_FILE_PATH, 'w') as f:
                    json.dump(dump, f, indent=4, separators=(', ', ': '))
            logging.debug('MyJson: save json complete')
            return True
        except:
            logging.debug('MyJson: Save json failed: %s' % sys.exc_info()[1])
            return False
