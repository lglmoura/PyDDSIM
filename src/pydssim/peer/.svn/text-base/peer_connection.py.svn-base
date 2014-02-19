'''
Created on 08/01/2010

@author: LGustavo
'''

import socket
import struct
#import threading
#import time
import traceback
from pydssim.util.log.peer_logger import PeerLogger

class PeerConnection:

   
    def __init__( self, peerId, host, port, sock=None):
   
        
        self.__id = peerId
        self.__host = host
        self.__port = port
       
        if not sock:
            self.__socket = socket.socket( socket.AF_INET, socket.SOCK_STREAM )
            self.__socket.connect( ( host, int(port) ) )
            
        else:
            self.__socket = sock
         
        self.__socketd = self.__socket.makefile( 'rw', 0 )
        #PeerLogger().resgiterLoggingInfo("PeersConnection from (%s,%s)" % (host,port))


    
    def __makeMSG( self, msgType, msgData ):
    
    
        #print "Peer conect ------------------->>>>  ",msgData
        msgLen = len(msgData)
        msg = struct.pack( "!4sL%ds" % msgLen, msgType, msgLen, msgData )
        return msg


    
    def sendData( self, msgType, msgData ):
    
        """
        senddata( message type, message data ) -> boolean status
    
        Send a message through a peer connection. Returns True on success
        or False if there was an error.
        """
    
        try:
           
            msg = self.__makeMSG( msgType, msgData )
            self.__socketd.write( msg )
            self.__socketd.flush()
            
        except KeyboardInterrupt:
            raise
        except:
            traceback.print_exc()
            return False
        return True
        
    def getHost(self):
        return self.__host
    
    def getPort(self):
        return self.__port 
    
    def getSocket(self):
        return self.__socket
    
    def recvData( self ):
        
        """
        recvdata() -> (msgType, msgData)
    
        Receive a message from a peer connection. Returns (None, None)
        if there was any error.
        """
      
        try:
           
            msgType = self.__socketd.read( 4 )
            if not msgType: 
                return (None, None)
            lenstr = self.__socketd.read( 4 )
            msgLen = int(struct.unpack( "!L", lenstr )[0])
            msg = ""
    
            while len(msg) != msgLen:
                data = self.__socketd.read( min(2048, msgLen - len(msg)) )
                if not len(data):
                    break
                msg += data
    
            if len(msg) != msgLen:
                return (None, None)
    
        except KeyboardInterrupt:
            raise
        except:
            traceback.print_exc()
            return (None, None)
    
        return ( msgType, msg )
    
        

    
    def close( self ):
   
        """
        close()
    
        Close the peer connection. The send and recv methods will not work
        after this call.
        """
    
        self.__socket.close()
        self.__socket = None
        self.__socketd = None


    def getID(self):
        return self.__id
    
    def getHost(self):
        return self.__host
    
    def getPort(self):
        return self.__port
    def __str__( self ):
   
           return "|%s|" % self.getID()




