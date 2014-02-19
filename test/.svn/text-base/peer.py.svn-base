'''
Created on 29/01/2010

@author: LGustavo
'''
from random import randint
class Peer():
    
    def __init__( self, id = 0):
        
        self.__neighbor = {}
        #127.0.0.1:
        self.__id = "%s"%id
        self.__levelNeighbor = 1
        
    def getID(self):
        return self.__id
    
    def getLevelNeighbor(self):
        return self.__levelNeighbor
    
    def getNeighbor(self):
        return self.__neighbor
    
    def setLevelNeighbor(self,level):
        
        while self.__hasLevelNeighbor(level):
           level+=1 
        self.__levelNeighbor = level
    
    def addNeighbor(self,id,level=1):
        
        if not (id in self.getNeighbor().keys()):
            self.getNeighbor()[id]= level
            
           
    
    def __discoverMinLevel(self):
        
        if max(self.getNeighbor().values())> self.getLevelNeighbor():
            return self.getLevelNeighbor()
    
    def __hasLevelNeighbor(self,level):
          
          return level in self.getNeighbor().values()
       
    def __hasPeerNeighbor(self,peer):
        
          return peer.getID() in self.getNeighbor().keys()
         
        
    def getSuperPeerWithLevel(self,peers,level):
        return dict([(peerID,(pLevel,peer)) for peerID, (pLevel,peer) in peers.iteritems() if (pLevel == level and peerID != self.getID())])
    
 
    
    def discoverNewNeighbor(self,portal,dportal):
       
        peers = portal.getSuperPeers()
         
        auxLevel = self.getLevelNeighbor()
         
        while dportal >= auxLevel:
            
            peerLevel =  self.getSuperPeerWithLevel(peers, auxLevel)
            
            if (not peerLevel) :
               auxLevel+=1
               continue 
            
            if (peerLevel) and (self.__hasLevelNeighbor(auxLevel)):
               auxLevel+=1
               continue 
             
            id,(level,peer) = peerLevel.popitem()
            
            if (self.__hasPeerNeighbor(peer)):
               auxLevel+=1
               continue
            
            self.addNeighbor(id, level)
            peer.addNeighbor(self.getID(),level) 
            
            if self.getLevelNeighbor() == level:
               self.setLevelNeighbor(self.getLevelNeighbor()+1)
               portal.addSuperPeer(self)
            
            peer.setLevelNeighbor(level+1)
            portal.addSuperPeer(peer)
            #print "peerid", self.getID()
            #print "SID Neig level",self.getID(),self.getNeighbor(),self.getLevelNeighbor()
            #print "PID Neig level",id,peer.getNeighbor(),peer.getLevelNeighbor()
            #print " "
 
             
           
            
    