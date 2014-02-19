'''
Created on 18/01/2010

@author: LGustavo
'''
#!/usr/bin/python

# btgui.py by Nadeem Abdul Hamid

"""
Module implementing simple BerryTella GUI for a simple p2p network.
"""


import sys
import threading


from random import *

#from btfiler import *
from peerdss import PeerDSS

class Gui():
   def __init__( self, firstpeer, hops=8, maxpeers=5, serverport=5678, master=None ):
 
    
      self.btpeer = PeerDSS( maxpeers, serverport )
      self.peerList = []
      
     
      
      host,port = firstpeer.split(':')
      self.btpeer.buildPeers( host, int(port), hops=hops )
      self.updatePeerList()
      
      t = threading.Thread( target = self.btpeer.mainLoop, args = [] )
      t.start()
      
      self.btpeer.startStabilizer( self.btpeer.checkLivePeers, 3 )
#      self.btpeer.startstabilizer( self.onRefresh, 3 )

      
   
      
   def __onDestroy( self, event ):
      self.btpeer.shutdown = True


   def updatePeerList( self ):
      if self.peerList.__len__() > 0:
         self.peerList.delete(0, self.peerList.size() - 1)
      for p in self.btpeer.getPeerIDs():
         print p
         self.peerList.insert( END, p )


     
      
      
   def onAdd(self):
      file = self.addfileEntry.get()
      if file.lstrip().rstrip():
         filename = file.lstrip().rstrip()
         self.btpeer.addlocalfile( filename )
      self.addfileEntry.delete( 0, len(file) )
      self.updateFileList()


   def onSearch(self):
      key = self.searchEntry.get()
      self.searchEntry.delete( 0, len(key) )

      for p in self.btpeer.getpeerids():
         self.btpeer.sendtopeer( p, 
                                 QUERY, "%s %s 4" % ( self.btpeer.myid, key ) )


   def onFetch(self):
      sels = self.fileList.curselection()
      if len(sels)==1:
         sel = self.fileList.get(sels[0]).split(':')
         if len(sel) > 2:  # fname:host:port
            fname,host,port = sel
            resp = self.btpeer.connectandsend( host, port, FILEGET, fname )
            if len(resp) and resp[0][0] == REPLY:
               fd = file( fname, 'w' )
               fd.write( resp[0][1] )
               fd.close()
               self.btpeer.files[fname] = None  # because it's local now


   def onRemove(self):
      sels = self.peerList.curselection()
      if len(sels)==1:
         peerid = self.peerList.get(sels[0])
         self.btpeer.sendtopeer( peerid, PEERQUIT, self.btpeer.myid )
         self.btpeer.removepeer( peerid )


   def onRefresh(self):
      self.updatePeerList()
      


   def onRebuild(self):
      if not self.btpeer.maxpeersreached():
         
         peerid = peerid.lstrip().rstrip()
         try:
            host,port = peerid.split(':')
            #print "doing rebuild", peerid, host, port
            self.btpeer.buildpeers( host, port, hops=3 )
         except:
            if self.btpeer.debug:
               traceback.print_exc()
#         for peerid in self.btpeer.getpeerids():
#            host,port = self.btpeer.getpeer( peerid )






def main():
   '''
      if len(sys.argv) < 4:
      print "Syntax: %s server-port max-peers peer-ip:port" % sys.argv[0]
      sys.exit(-1)
   
   '''
   
   serverport = 5000 #int(sys.argv[1])
   maxpeers = 8# sys.argv[2]
   peerid = "127.0.0.1:4000"#sys.argv[3]
   app = Gui( firstpeer=peerid, maxpeers=maxpeers, serverport=serverport )
   
   serverport = 6000 #int(sys.argv[1])
   maxpeers = 8# sys.argv[2]
   peerid = "127.0.0.1:5000"#sys.argv[3]
   app1 = Gui( firstpeer=peerid, maxpeers=maxpeers, serverport=serverport )

# setup and run app
if __name__=='__main__':
   main()
