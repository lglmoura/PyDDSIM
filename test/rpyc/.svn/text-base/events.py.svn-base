'''
Created on 05/01/2010

@author: LGustavo
'''
import rpyc
import os
import time
from threading import Thread
 
class FileMonitorService(rpyc.Service):
    class exposed_FileMonitor(object):   # exposing names is not limited to methods :)
        def __init__(self, filename, callback, interval = 1):
            self.filename = filename
            self.interval = interval
            self.last_stat = None
            self.callback = rpyc.async(callback)   # create an async callback
            self.active = True
            self.thread = Thread(target = self.work)
            self.thread.start()
        def exposed_stop(self):   # this method has to be exposed too
            self.active = False
            self.thread.join()
        def work(self):
            while self.active:
                stat = os.stat(self.filename)
                if self.last_stat is not None and self.last_stat != stat:
                    self.callback(self.last_stat, stat)   # notify the client of the change
                self.last_stat = stat
                time.sleep(self.interval)
                
 
class TimeService(rpyc.Service):
    def exposed_gettime(self):
        return time.time()                
 
if __name__ == "__main__":
    from rpyc.utils.server import ThreadedServer
    #ThreadedServer(TimeService, port = 18871).start()
    ThreadedServer(TimeService).start()
