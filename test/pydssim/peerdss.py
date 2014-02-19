'''
Created on 07/01/2010

@author: LGustavo
'''

from peer import Peer
from peer_connection import PeerConnection
import traceback

PEERNAME = "NAME"   # request a peer's canonical id
LISTPEERS = "LIST"
INSERTPEER = "JOIN"
QUERY = "QUER"
QRESPONSE = "RESP"
FILEGET = "FGET"
PEERQUIT = "QUIT"
SUPERPEER    = "SUPE"
REPLY = "REPL"
ERROR = "ERRO"
PEERFULL = "PEFU"




class PeerDSS(Peer):

    """ Implements a file-sharing peer-to-peer entity based on the generic
    BerryTella P2P framework.

    """


    def __init__(self, maxPeers, serverPort):
   
   
        Peer.__init__(self, maxPeers, serverPort)
        
        self.files = {}  # available files: name --> peerid mapping
    
        self.addRouter(self.__router)
    
        handlers = {LISTPEERS : self.__handle_listpeers,
                INSERTPEER : self.__handle_insertpeer,
                PEERNAME: self.__handle_peername,
                QUERY: self.__handle_query,
                QRESPONSE: self.__handle_qresponse,
                FILEGET: self.__handle_fileget,
                PEERQUIT: self.__handle_quit,
                SUPERPEER: self.__handle_superpeer
               }
        for mt in handlers:
            self.addHandler(mt, handlers[mt])

  
    
    def __router(self, peerID):
    
        if peerID not in self.getPeerIDs():
            return (None, None, None)
        else:
            rt = [peerID]
            rt.extend(self.peers[peerID])
            return rt



    
    def __handle_insertpeer(self, peerConn, data):
    
        """ Handles the INSERTPEER (join) message type. The message data
        should be a string of the form, "peerid  host  port", where peer-id
        is the canonical name of the peer that desires to be added to this
        peer's list of peers, host and port are the necessary data to connect
        to the peer.
    
        """
        self.getPeerLock().acquire()
        try:
            try:
                
                peerID,super,host,port = data.split()
                
               
                 
                if self.maxPeersReached() and peerID != super:
                    #print 'maxPeers %d reached: connection terminating' % self.getMaxPeers()
                    #peerConn.sendData(ERROR, 'Join: too many peers')
                    peerConn.sendData(PEERFULL ,self.getMySuperPeer())
                    return
                 
                #peerid = '%s:%s' % (host,port)
                if peerID not in self.getPeerIDs() and peerID != self.getMyID():
                  
                    self.addPeer(peerID, host, port,super)
                    
                    peerConn.sendData(REPLY, 'Join: peer added: %s' % peerID)
                    peerConn.sendData(SUPERPEER,"%s"%self.getMySuperPeer())
                else:
                   
                    peerConn.sendData(ERROR, 'Join: peer already inserted %s'
                               % peerID)
            except:
                print 'invalid insert %s: %s' % (str(peerConn), data)
                peerConn.sendData(ERROR, 'Join: incorrect arguments')
        finally:
            self.getPeerLock().release()

    def __handle_listpeers(self, peerConn, data):
        
        """ Handles the LISTPEERS message type. Message data is not used. """

        self.getPeerLock().acquire()
        try:
            #print 'Listing peers %d' % self.numberOfPeers()
            peerConn.sendData(REPLY, '%d' % self.numberOfPeers())
            for pid in self.getPeerIDs():
                host,port,super = self.getPeer(pid)
                
                peerConn.sendData(REPLY, '%s %s %d %s' % (pid, host, port, super))
        finally:
            self.getPeerLock().release()



    
    def __handle_peername(self, peerConn, data):
    
       """ Handles the NAME message type. Message data is not used. """
       peerConn.sendData(REPLY, self.getMyID())
        
    def __handle_superpeer(self, peerConn, data):
    
        
        self.getPeerLock().acquire()
        try:
            try:
                
                super = data.split()
                print " super ",super
                 
                if self.getMySuperPeer() == Peer.NULL:
                    self.setMySuperPeer(super)                    
                    return
                
            except:
                print 'invalid insert %s: %s' % (str(peerConn), data)
                peerConn.sendData(ERROR, 'Super: incorrect arguments')
        finally:
            self.getPeerLock().release()    


    def __handle_query(self, peerConn, data):

        """ Handles the QUERY message type. The message data should be in the
        format of a string, "return-peer-id  key  ttl", where return-peer-id
        is the name of the peer that initiated the query, key is the (portion
        of the) file name being searched for, and ttl is how many further 
        levels of peers this query should be propagated on.
    
        """
        # self.peerlock.acquire()
        try:
            peerID, key, ttl = data.split()
            peerConn.sendData(REPLY, 'Query ACK: %s' % key)
        except:
            #print 'invalid query %s: %s' % (str(peerConn), data)
            peerConn.sendData(ERROR, 'Query: incorrect arguments')
        # self.peerlock.release()
    
        t = threading.Thread(target=self.__processquery, 
                      args=[peerID, key, int(ttl)])
        t.start()


    def __processquery(self, peerID, key, ttl):

        """ Handles the processing of a query message after it has been 
        received and acknowledged, by either replying with a QRESPONSE message
        if the file is found in the local list of files, or propagating the
        message onto all immediate neighbors.
    
        """
        for fname in self.files.keys():
            if key in fname:
                fpeerID = self.files[fname]
                if not fpeerID:   # local files mapped to None
                    fpeerID = self.getMyId()
            host,port = peerID.split(':')
            # can't use sendtopeer here because peerID is not necessarily
            # an immediate neighbor
            self.connectAndSend(host, int(port), QRESPONSE, 
                         '%s %s' % (fname, fpeerID),
                         pid=peerID)
            return
        # will only reach here if key not found... in which case
        # propagate query to neighbors
        if ttl > 0:
            msgData = '%s %s %d' % (peerID, key, ttl - 1)
            for nextpid in self.getPeerIDs():
                self.sendToPeer(nextpid, QUERY, msgData)



    
    def __handle_qresponse(self, peerConn, data):
    
        """ Handles the QRESPONSE message type. The message data should be
        in the format of a string, "file-name  peer-id", where file-name is
        the file that was queried about and peer-id is the name of the peer
        that has a copy of the file.
    
        """
        try:
            fname, fpeerID = data.split()
            if fname in self.files:
                print 'Can\'t add duplicate file %s %s' %  (fname, fpeerID)
            else:
                self.files[fname] = fpeerID
        except:
            #if self.debug:
            #traceback.print_exc()
            pass


    def __handle_fileget(self, peerConn, data):

        """ Handles the FILEGET message type. The message data should be in
        the format of a string, "file-name", where file-name is the name
        of the file to be fetched.
    
        """
        fname = data
        if fname not in self.files:
            print 'File not found %s' % fname
            peerConn.sendData(ERROR, 'File not found')
            return
        try:
            fd = file(fname, 'r')
            filedata = ''
            while True:
                data = fd.read(2048)
                if not len(data):
                    break;
                filedata += data
            fd.close()
        except:
            print 'Error reading file %s' % fname
            peerConn.sendData(ERROR, 'Error reading file')
            return
        
        peerConn.sendData(REPLY, filedata)

    def __handle_quit(self, peerConn, data):

        """ Handles the QUIT message type. The message data should be in the
        format of a string, "peer-id", where peer-id is the canonical
        name of the peer that wishes to be unregistered from this
        peer's directory.
    
        """
        self.__peerLock.acquire()
        try:
            peerID = data.lstrip().rstrip()
            if peerID in self.getpeerIDs():
                msg = 'Quit: peer removed: %s' % peerID 
                print msg
                peerConn.sendData(REPLY, msg)
                self.removepeer(peerID)
            else:
                msg = 'Quit: peer not found: %s' % peerID 
                print msg
                peerConn.sendData(ERROR, msg)
        finally:
            self.__peerlock.release()



    def buildSuperPeer(self,host, port, hops):
        
        """ buildpeers(host, port, hops) 
    
        Attempt to build the local peer list up to the limit stored by
        self.maxPeers, using a simple depth-first search given an
        initial host and port as starting point. The depth of the
        search is limited by the hops parameter.
    
        """
       
    
        print "Building Super peers from (%s,%s)" % (host,port)
    
        try:
            #print "contacting " #+ peerID
            _, peerID = self.connectAndSend(host, port, PEERNAME, '')[0]
    
            #print "contacted " + peerID
            resp = self.connectAndSend(host, port, INSERTPEER, 
                        '%s %s %s %d' % (self.getMyID(),self.getMySuperPeer(),
                                  self.getServerHost(), 
                                  self.getServerPort()))#[0]
           
            
            if (resp[0][0] != REPLY) or (peerID in self.getPeerIDs()):
                return
            
            print "rest super",resp           
            self.addPeer(peerID, host, port,resp[1][1])
            
            
        except:
            #traceback.print_exc()
            #print "eerrroooo" 
            self.removePeer(peerID)
    
    
        
        
        
    def buildPeers(self, host, port, hops=1):
    
        """ buildpeers(host, port, hops) 
    
        Attempt to build the local peer list up to the limit stored by
        self.maxPeers, using a simple depth-first search given an
        initial host and port as starting point. The depth of the
        search is limited by the hops parameter.
    
        """
        if self.maxPeersReached() or not hops:
            return
    
        peerID = None
    
        print "Building peers from (%s,%s)" % (host,port)
    
        try:
            #print "contacting " #+ peerID
            _, peerID = self.connectAndSend(host, port, PEERNAME, '')[0]
    
            #print "contacted " + peerID
            resp = self.connectAndSend(host, port, INSERTPEER, 
                        '%s %s %s %d' % (self.getMyID(),self.getMySuperPeer(),
                                  self.getServerHost(), 
                                  self.getServerPort()))#[0]
           
            
            if (resp[0][0] != REPLY) or (peerID in self.getPeerIDs()):
                
                if resp[0][0] == PEERFULL:
                    
                    self.setMySuperPeer(self.getMyID())
                    self.setPeerType(Peer.SUPER)
                    shost,sport = resp[0][1].split(":")
                   
                    self.buildSuperPeer(shost, sport, hops)
                return
            
            
            if (resp[1][0] == SUPERPEER) and self.getMySuperPeer() == Peer.NULL:
                self.setMySuperPeer(resp[1][1])
                 
            
            self.addPeer(peerID, host, port,resp[1][1])
            
            
    
    
            # do recursive depth first search to add more peers
            resp = self.connectAndSend(host, port, LISTPEERS, '',
                        pid=peerID)
            
            if len(resp) > 1:
                resp.reverse()
            resp.pop()    # get rid of header count reply
            
            print "Responta ", resp
            
            while len(resp):
                nextpid,host,port,super = resp.pop()[1].split()
                
                
                if nextpid != self.getMyID():
                    self.buildPeers(host, port, hops - 1)
        except:
            #traceback.print_exc()
            #print "eerrroooo" 
            self.removePeer(peerID)
    
    
    
       
    def addLocalFile(self, filename):
    
        """ Registers a locally-stored file with the peer. """
        self.files[filename] = None
        self.__debug("Added local file %s" % filename)
