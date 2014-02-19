#!/usr/bin/python

# btgui.py by Nadeem Abdul Hamid

"""
Module implementing simple BerryTella GUI for a simple p2p network.
"""


import sys
import threading

from Tkinter import *
from random import *

from peerdss import *


class Gui(Frame):
   def __init__( self, firstpeer, hops=8, maxpeers=5, serverport=5678, master=None ):
 
    
      Frame.__init__( self, master )
      
      self.grid()
      self.createWidgets()
      self.master.title( "BerryTella Filer GUI %d" % serverport )
      self.btpeer = PeerDDS( maxpeers, serverport )
      
      self.bind( "<Destroy>", self.__onDestroy )
      
      host,port = firstpeer.split(':')
      print host,port
      self.btpeer.buildPeers( host, int(port), hops=hops )
      self.updatePeerList()
      
      t = threading.Thread( target = self.btpeer.mainLoop, args = [] )
      t.start()
      
      self.btpeer.startStabilizer( self.btpeer.checkLivePeers, 3 )
#      self.btpeer.startstabilizer( self.onRefresh, 3 )
      self.after( 3000, self.onTimer )
      
      
   def onTimer( self ):
      self.onRefresh()
      self.after( 3000, self.onTimer )
      #self.after_idle( self.onTimer )

      
   def __onDestroy( self, event ):
      self.btpeer.shutdown = True


   def updatePeerList( self ):
      if self.peerList.size() > 0:
         self.peerList.delete(0, self.peerList.size() - 1)
      for p in self.btpeer.getPeerIDs():
         print p
         self.peerList.insert( END, p )


   def updateFileList( self ):
      if self.fileList.size() > 0:
         self.fileList.delete(0, self.fileList.size() - 1)
      for f in self.btpeer.files:
         p = self.btpeer.files[f]
         if not p:
            p = '(local)'
         self.fileList.insert( END, "%s:%s" % (f,p) )
      
      
   def createWidgets( self ):
      """
      Set up the frame widgets
      """
      fileFrame = Frame(self)
      peerFrame = Frame(self)

      rebuildFrame = Frame(self)
      searchFrame = Frame(self)
      addfileFrame = Frame(self)
      pbFrame = Frame(self)
      
      fileFrame.grid(row=0, column=0, sticky=N+S)
      peerFrame.grid(row=0, column=1, sticky=N+S)
      pbFrame.grid(row=2, column=1)
      addfileFrame.grid(row=3)
      searchFrame.grid(row=4)
      rebuildFrame.grid(row=3, column=1)
      
      Label( fileFrame, text='Available Files' ).grid()
      Label( peerFrame, text='Peer List' ).grid()
      
      fileListFrame = Frame(fileFrame)
      fileListFrame.grid(row=1, column=0)
      fileScroll = Scrollbar( fileListFrame, orient=VERTICAL )
      fileScroll.grid(row=0, column=1, sticky=N+S)

      self.fileList = Listbox(fileListFrame, height=5, 
                        yscrollcommand=fileScroll.set)
      #self.fileList.insert( END, 'a', 'b', 'c', 'd', 'e', 'f', 'g' )
      self.fileList.grid(row=0, column=0, sticky=N+S)
      fileScroll["command"] = self.fileList.yview

      self.fetchButton = Button( fileFrame, text='Fetch',
                           command=self.onFetch)
      self.fetchButton.grid()
      
      self.addfileEntry = Entry(addfileFrame, width=25)
      self.addfileButton = Button(addfileFrame, text='Add',
                           command=self.onAdd)
      self.addfileEntry.grid(row=0, column=0)
      self.addfileButton.grid(row=0, column=1)
      
      self.searchEntry = Entry(searchFrame, width=25)
      self.searchButton = Button(searchFrame, text='Search', 
                           command=self.onSearch)
      self.searchEntry.grid(row=0, column=0)
      self.searchButton.grid(row=0, column=1)
      
      peerListFrame = Frame(peerFrame)
      peerListFrame.grid(row=1, column=0)
      peerScroll = Scrollbar( peerListFrame, orient=VERTICAL )
      peerScroll.grid(row=0, column=1, sticky=N+S)
      
      self.peerList = Listbox(peerListFrame, height=5,
                        yscrollcommand=peerScroll.set)
      #self.peerList.insert( END, '1', '2', '3', '4', '5', '6' )
      self.peerList.grid(row=0, column=0, sticky=N+S)
      peerScroll["command"] = self.peerList.yview
      
      self.removeButton = Button( pbFrame, text='Remove',
                                  command=self.onRemove )
      self.refreshButton = Button( pbFrame, text = 'Refresh', 
                            command=self.onRefresh )

      self.rebuildEntry = Entry(rebuildFrame, width=25)
      self.rebuildButton = Button( rebuildFrame, text = 'Rebuild', 
                            command=self.onRebuild )
      self.removeButton.grid(row=0, column=0)
      self.refreshButton.grid(row=0, column=1)
      self.rebuildEntry.grid(row=0, column=0)
      self.rebuildButton.grid(row=0, column=1)      
      
      
      # print "Done"
      
      
   def onAdd(self):
      file = self.addfileEntry.get()
      if file.lstrip().rstrip():
         filename = file.lstrip().rstrip()
         self.btpeer.addLocalFile( filename )
      self.addfileEntry.delete( 0, len(file) )
      self.updateFileList()


   def onSearch(self):
      key = self.searchEntry.get()
      self.searchEntry.delete( 0, len(key) )

      for p in self.btpeer.getPeerIDs():
         self.btpeer.sendToPeer( p, 
                                 QUERY, "%s %s 4" % ( self.btpeer.__myID, key ) )


   def onFetch(self):
      sels = self.fileList.curselection()
      if len(sels)==1:
         sel = self.fileList.get(sels[0]).split(':')
         if len(sel) > 2:  # fname:host:port
            fname,host,port = sel
            resp = self.btpeer.connectAndSend( host, port, FILEGET, fname )
            if len(resp) and resp[0][0] == REPLY:
               fd = file( fname, 'w' )
               fd.write( resp[0][1] )
               fd.close()
               self.btpeer.files[fname] = None  # because it's local now


   def onRemove(self):
      sels = self.peerList.curselection()
      if len(sels)==1:
         peerid = self.peerList.get(sels[0])
         self.btpeer.sendToPeer( peerid, PEERQUIT, self.btpeer.__myID )
         self.btpeer.removePeer( peerid )


   def onRefresh(self):
      self.updatePeerList()
      self.updateFileList()


   def onRebuild(self):
      if not self.btpeer.maxPeersReached():
         peerid = self.rebuildEntry.get()
         self.rebuildEntry.delete( 0, len(peerid) )
         peerid = peerid.lstrip().rstrip()
         try:
            host,port = peerid.split(':')
            #print "doing rebuild", peerid, host, port
            self.btpeer.buildPeers( host, port, hops=3 )
         except:
            if False:
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
   app.mainloop()


# setup and run app
if __name__=='__main__':
   main()
