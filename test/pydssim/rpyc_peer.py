'''
Created on 05/01/2010

@author: LGustavo
'''

from __future__ import with_statement
from rpyc import Service, async
from rpyc.utils.server import ThreadedServer
from threading import RLock


broadcast_lock = RLock()
tokens = set()


from pydssim.peer.abstract_peer import AbstractPeer
from pydssim.util.decorator.public import createURN
from pydssim.util.logger import Logger

class RPyCPeer(AbstractPeer,Service):
    """
    Implements the basic functions of a RPyC peer.
    @author: Luiz Gustavo
    @organization: Federal University of Rio de Janeiro
    @contact: lglmoura@cos.ufrj.br 
    @since: 05/01/2010
    """

    def __init__(self,network, pid=createURN("rpycpeer"),udpPort=4000):
        
        AbstractPeer.initialize(self,  network, pid,udpPort)
  
    
    def createConnection(self, target):
        if not self.isConnected(target) and self.countNeighbor() <= self.getNetwork().getMaxNeighbor() :
            AbstractPeer.createConnection(self,target)
            try:
                self.conn = rpyc.connect(target.getIPAddress(), target.getPort())
                Logger().resgiterLoggingInfo("Conectioned in  peers IP = %s  Port = %s"%(target.getIPAddress(), target.getPort()))
            except Exception:
                self.conn = None
                Logger().resgiterLoggingInfo("Not Conectioned in  peers IP = %s  Port = %s"%(target.getIPAddress(), target.getPort()))
                '''m=gtk.MessageDialog(buttons = gtk.BUTTONS_OK, 
                    type = gtk.MESSAGE_ERROR, 
                    flags = gtk.DIALOG_MODAL | gtk.DIALOG_DESTROY_WITH_PARENT, 
                    message_format="Connection refused")
                m.run()
                m.destroy()
                '''
                return
            
        
    def on_connect(self):
        
        '''
           conexion receives and verifies that is 
           already connected to this peer 
        '''
        
        self.token = None
    
    def on_disconnect(self):
        if self.token:
            self.token.exposed_logout()
    
    def exposed_login(self, username, password, callback):
        if self.token and not self.token.stale:
            raise ValueError("already logged in")
        if username in USERS_DB and password == USERS_DB[username]:
            self.token = UserToken(username, async(callback))
            return self.token
        else:
            raise ValueError("wrong username or password")