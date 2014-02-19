#!/usr/bin/python

import socket
import struct
import threading
import time
import traceback
from peer_connection import PeerConnection



class Peer:
    """ Implements the core functionality that might be used by a peer in a
    P2P network.

    """
    NUMBER = 1
    SUPER  = "SUPER_PEER"
    SIMPLE = "SIMPLE_PEER"
    NULL   = "NULL"


    
    def __init__( self, maxPeers=7, serverPort=3000, myID=None, serverHost = None, peerType = SIMPLE, mySuperPeer = NULL ):
   
    	""" Initializes a peer servent (sic.) with the ability to catalog
    	information for up to maxpeers number of peers (maxpeers may
    	be set to 0 to allow unlimited number of peers), listening on
    	a given server port , with a given canonical peer name (id)
    	and host address. 
    
    	"""
    	
        self.__peerType = peerType
        self.__mySuperPeer = mySuperPeer
    	self.__maxPeers = int(maxPeers)
    	self.__serverPort = int(serverPort)
        self.__attemptedConnectionNumber = 0
    	if serverHost:
            self.__serverHost = serverHost
    	else:
            self.__serverHost = socket.gethostbyname(socket.gethostname())
    
    	if myID:
            self.__myID = myID
    	else: 
            self.__myID = '%s:%d' % (self.__serverHost, self.__serverPort)
    
    	self.__peerLock = threading.Lock()  
    	self.__peers = {} 
                
    	self.__shutdown = False  
    
    	self.__handlers = {}
    	self.__router = None
    
    def getShutdown(self):
        return self.__shutdown
    
    def getRouter(self):
        return self.__router
    
    def getAttemptedConnectionNumber(self):
        return self.__attemptedConnectionNumber
    
    def setAttemptedConnectionNumber(num):
        self.__attemptedConnectionNumber = num
           
    def getMyID(self):
        return self.__myID
    
    def getMySuperPeer(self):
        return self.__mySuperPeer
    
    def setMySuperPeer(self,super):
        
        self.__mySuperPeer = super
    
    def getServerHost(self):
        return self.__serverHost
    
    def getServerPort(self):
        return self.__serverPort
    
    def getPeerLock(self):
        return self.__peerLock
    
    def getPeers(self):
        return self.__peers
    
    def getMaxPeers(self):
        return self.__maxPeers
    
    def getPeerType(self):
        return self.__peerType
    
    def setPeerType(self,type):
        
        self.__peerType = type
        
    
    def __handlepeer( self, clientSock ):
    
    	"""
    	handlepeer( new socket connection ) -> ()
    
    	Dispatches messages from the socket connection
    	"""
    
    	print 'New child ' + str(threading.currentThread().getName()) 
    	print 'Connected ' + str(clientSock.getpeername())
    
    	host, port = clientSock.getpeername()
    	peerConn = PeerConnection( None, host, port, clientSock)
    	
    	try:
    	    msgType, msgData = peerConn.recvData()
            
    	    if msgType: 
                msgType = msgType.upper()
    	    if msgType not in self.__handlers:
                print 'Not handled: %s: %s' % (msgType, msgData)
    	    else:
                print 'Handling peer msg: %s: %s' % (msgType, msgData)
                self.__handlers[ msgType ]( peerConn, msgData )
    	except KeyboardInterrupt:
    	    raise
    	except:
    	    
    		traceback.print_exc()
    	
    	print 'Disconnecting ' + str(clientSock.getpeername()) 
    	peerConn.close()

    
    def __runstabilizer( self, stabilizer, delay ):
    
    	while not self.__shutdown:
    	    stabilizer()
    	    time.sleep( delay )

	  
    def setMyID( self, myID ):
    
	       self.__myID = myID

  
    def startStabilizer( self, stabilizer, delay ):
    
    	""" Registers and starts a stabilizer function with this peer. 
    	The function will be activated every <delay> seconds. 
    
    	"""
    	t = threading.Thread( target = self.__runstabilizer, 
    			      args = [ stabilizer, delay ] )
    	t.start()

	

    
    def addHandler( self, msgType, handler ):
    
    	""" Registers the handler for the given message type with this peer """
        
    	assert len(msgType) == 4
    	self.__handlers[ msgType ] = handler



   
    def addRouter( self, router ):
    
    	""" Registers a routing function with this peer. The setup of routing
    	is as follows: This peer maintains a list of other known peers
    	(in self.peers). The routing function should take the name of
    	a peer (which may not necessarily be present in self.peers)
    	and decide which of the known peers a message should be routed
    	to next in order to (hopefully) reach the desired peer. The router
    	function should return a tuple of three values: (next-peer-id, host,
    	port). If the message cannot be routed, the next-peer-id should be
    	None.
    
    	"""
    	self.__router = router



   
    def addPeer( self, peerID, host, port, superPeer=NULL ):
    
    	""" Adds a peer name and host:port mapping to the known list of peers.
    	
    	"""
       
        if superPeer == Peer.NULL:
            superPeer = self.getMySuperPeer()
            
        
        
    	if peerID not in self.getPeers() and (self.getMaxPeers() == 0 or len(self.getPeers()) < self.getMaxPeers()):
    	    self.getPeers()[ peerID ] = (host, int(port),superPeer)
            
            
    	    return True
    	else:
    	    return False



    
    def getPeer( self, peerID ):
    
    	""" Returns the (host, port) tuple for the given peer name """
    	assert peerID in self.getPeers()    # maybe make this just a return NULL?
    	return self.getPeers()[ peerID ]



    
    def removePeer( self, peerID ):
    
    	""" Removes peer information from the known list of peers. """
    	if peerID in self.getPeers():
    	    del self.getPeers()[ peerID ]



    
    def addPeerAt( self, loc, peerID, host, port,super ):
    
    	""" Inserts a peer's information at a specific position in the 
    	list of peers. The functions addpeerat, getpeerat, and removepeerat
    	should not be used concurrently with addpeer, getpeer, and/or 
    	removepeer. 
    
    	"""
    	self.getPeers()[ loc ] = (peerID, host, int(port),super)



    
    def getPeerAt( self, loc ):
    
    	if loc not in self.getPeers():
    	    return None
    	return self.getPeers()[ loc ]



    
    def removePeerAt( self, loc ):
    
	       removePeer( self, loc ) 



    
    def getPeerIDs( self ):
    
    	""" Return a list of all known peer id's. """
    	return self.getPeers().keys()


    def numberOfPeers( self ):
   
    	""" Return the number of known peer's. """
    	return len(self.getPeers())
 
    def maxPeersReached( self ):
       
    	""" Returns whether the maximum limit of names has been added to the
    	list of known peers. Always returns True if maxPeers is set to
    	0.
    
    	"""
    	assert self.getMaxPeers() == 0 or len(self.getPeers()) <= self.getMaxPeers()
    	return self.getMaxPeers() > 0 and len(self.getPeers()) == self.getMaxPeers()


    def makeServerSocket( self, port, backlog=5 ):
  
    	""" Constructs and prepares a server socket listening on the given 
    	port.
    
    	"""
    	s = socket.socket( socket.AF_INET, socket.SOCK_STREAM )
    	s.setsockopt( socket.SOL_SOCKET, socket.SO_REUSEADDR, 1 )
    	s.bind( ( '', port ) )
    	s.listen( backlog )
    	return s


    def sendToPeer( self, peerID, msgType, msgData, waitreply=True ):
   
    	"""
    	sendtopeer( peer id, message type, message data, wait for a reply )
    	 -> [ ( reply type, reply data ), ... ] 
    
    	Send a message to the identified peer. In order to decide how to
    	send the message, the router handler for this peer will be called.
    	If no router function has been registered, it will not work. The
    	router function should provide the next immediate peer to whom the 
    	message should be forwarded. The peer's reply, if it is expected, 
    	will be returned.
    
    	Returns None if the message could not be routed.
    	"""
    
    	if self.__router:
    	    nextpid, host, port = self.__router( peerID )
    	if not self.__router or not nextpid:
    	    print 'Unable to route %s to %s' % (msgType, peerID)
    	    return None
    	#host,port = self.peers[nextpid]
    	return self.connectAndSend( host, port, msgType, msgData,
    				    pid=nextpid,
    				    waitreply=waitreply )
    


   
    def connectAndSend( self, host, port, msgType, msgData, 
			pid=None, waitreply=True ):
   
    	msgreply = []
        num = self.getAttemptedConnectionNumber()
        
        while  num != Peer.NUMBER:
            
            print "ConnectAndSend peers from (%s,%s) %s number %d" % (host,port,msgType,num)
            try:
                peerConn = PeerConnection( pid, host, port)
                peerConn.sendData( msgType, msgData )
                if waitreply:
                    onereply = peerConn.recvData()
                    while (onereply != (None,None)):
                        msgreply.append( onereply )
                        print 'Got reply %s: %s' % ( pid, str(msgreply) )
                        onereply = peerConn.recvData()
                peerConn.close()
                break
            except KeyboardInterrupt:
                raise
            except:
                num += 1
                print "Erro de Connecao peers from (%s,%s) %s %d" % (host,port,msgType, num)
        
        if num == Peer.NUMBER:
            self.setMySuperPeer(self.getMyID())
            self.setPeerType(Peer.SUPER)
            
    	return msgreply

  
    
    def checkLivePeers( self ):
    
    	""" Attempts to ping all currently known peers in order to ensure that
    	they are still active. Removes any from the peer list that do
    	not reply. This function can be used as a simple stabilizer.
    
    	"""
    	todelete = []
    	for pid in self.getPeers():
    	    isconnected = False
    	    try:
        		
        		host,port,super = self.getPeers()[pid]
        		peerConn = PeerConnection( pid, host, port)
        		peerConn.sendData( 'PING', '' )
        		isconnected = True
    	    except:
                todelete.append( pid )
    	    if isconnected:
                peerConn.close()
    
    	self.getPeerLock().acquire()
    	try:
    	    for pid in todelete: 
                if pid in self.getPeers():
                    del self.getPeers()[pid]
    	finally:
    	    self.getPeerLock().release()
        



   
    def mainLoop( self ):
           
    	s = self.makeServerSocket( self.getServerPort() )
    	s.settimeout(1)
    	print 'Server started: %s (%s:%d)'  % ( self.getMyID(), self.getServerHost(), self.getServerPort() )
    	
    	while not self.getShutdown():
            #print "Server started: %s (%s:%d)"%(self.myID, self.serverHost, self.serverPort)
    	    try:
        		#print ('Listening for connections...' )
               
        		clientSock, clientAddr = s.accept()
        		clientSock.settimeout(None)
        
        		t = threading.Thread( target = self.__handlepeer,
        				      args = [ clientSock ] )
        		t.start()
    	    except KeyboardInterrupt:
        		print 'KeyboardInterrupt: stopping mainloop'
        		self.getShutdown = True
        		continue
    	    except:
    		
    		    #traceback.print_exc()
    		    continue
    
    	
    	print 'Main loop exiting' 
    
    	s.close()