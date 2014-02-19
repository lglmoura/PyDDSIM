'''
Created on 29/01/2010

@author: LGustavo
'''

import math
from portal import Portal
from peer import Peer
from random import random,randint,shuffle

#
#
def find_key(dic, val):
    return dict([(k,v) for k, v in dic.iteritems() if v == val])#[0]


if __name__ == '__main__':
    #print math.log(5,2)
    #print math.trunc(math.log(5,2))
    portal = Portal()
   
    print randint(5,10)
   
    for i in range(1,9):
        peer = Peer(i)
        #portal.addSuperPeer(peer.getID(),peer.getLevelNeighbor())
        
        portal.addSuperPeer(peer)
        peer.discoverNewNeighbor(portal, portal.getDimension())
    
       
    for (peerID,(level,peer)) in portal.getSuperPeers().iteritems():
        print peerID,level,peer
        for npeerID,nlevel in peer.getNeighbor().iteritems():
            print npeerID,"->",nlevel
   
   
    
       
       
        
        