'''
Created on 07/01/2010

@author: LGustavo
'''
import threading
from time import sleep, ctime
from filergui import BTGui 
from btfiler import *

def startGui(peerid,maxpeers,serverport):
    
    app = BTGui( firstpeer=peerid, maxpeers=maxpeers, serverport=serverport )
    
    app.mainloop()
    sleep(randint(1,6))

class test:
    
    def __init__( self, firstpeer,  maxpeers=5, serverport=5678):
        self.testx(firstpeer,  maxpeers, serverport)
    
    def testx(self,firstpeer,  maxpeers=5, serverport=5678,hops=8):
       
       print firstpeer, maxpeers, serverport
       self.btpeer = FilerPeer( maxpeers, serverport )
       
       host,port = firstpeer.split(':')
       self.btpeer.buildpeers( host, int(port), hops=hops )
          
       t = threading.Thread( target = self.btpeer.mainloop, args = [] )
       t.start()
       
       self.btpeer.startstabilizer( self.btpeer.checklivepeers, 3 )
    #      self.btpeer.startstabilizer( self.onRefresh, 3 )
       

def main():
    print 'starting at:', ctime()
    threads = []
    #nloops = range(len(loops))
    nloops = range(0,7)
    serverport = 3999
    for i in nloops:
       
        maxpeers = 8
        peerid = "127.0.0.1:%s"%(serverport)
        serverport +=1
        t = threading.Thread(target=test,
        args=((peerid,maxpeers,serverport)))
        threads.append(t)

    for i in nloops:            # start threads
        threads[i].start()

    for i in nloops:            # wait for all
        threads[i].join()       # threads to finish
        
   
    
    print 'all DONE at:', ctime()
    
if __name__ == '__main__':
    main()