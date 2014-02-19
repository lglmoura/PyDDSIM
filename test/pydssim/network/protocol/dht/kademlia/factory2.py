'''
Created on 04/01/2010

@author: LGustavo
'''

import os, sys, time, signal
from pydssim.network.protocol.dht.dht_peer import DHTPeer
from pydssim.network.p2p_network import P2PNetwork
from pydssim.peer.default_peer import DefaultPeer
import uuid

import twisted.internet.reactor

def destroyNetwork(peers):
    pass


def createPeer(port=4000,ipaddress=None,startport=None,net=None):
    #import twisted.internet.reactor
    import sys, os

    if ipaddress != None:
        knownPeers = [(ipaddress, startport)]
        
    else:
        knownPeers = None

    #print knownPeers, port
    urn = "urn:peer:id:"+uuid.uuid1().__str__()
    
    peer = DefaultPeer(net,urn,port)
    #peer = DHTPeer(udpPort=port)
    
    #peer.joinNetwork(knownPeers)
    dhtpeer = peer.getDHTPeer()
    
    dhtpeer.joinNetwork(knownPeers)
    #peer.printNeighbors()
    #print port,ipaddress,startPort
    

if __name__ == '__main__':
    
    net1 = P2PNetwork(None, 50, 3000, 7)
        
    amount = 5 #int(sys.argv[1])
    
    import socket
    ipAddress = socket.gethostbyname(socket.gethostname())
    print 'Network interface IP address omitted; using %s   ...' % ipAddress

    startPort = 4000
    port = startPort+1
    peers = []
    print 'Creating Kademlia network...'
    try:
        
        createPeer(port=startPort,net=net1)
        
        for i in range(amount-1):
            
            time.sleep(0.15)
            hashAmount = i*50/amount
            hashbar = '#'*hashAmount
            output = '\r[%-50s] %d/%d ' % (hashbar, i, amount)
            sys.stdout.write(output)
           
            createPeer(port,ipAddress,startPort,net1)
            
            port += 1
            
       
    except KeyboardInterrupt:
        '\nNetwork creation cancelled.'
        destroyNetwork(peers)
        sys.exit(1)
    
    print '\n\n---------------\nNetwork running\n---------------\n'
    twisted.internet.reactor.run()
    try:
        while 1:
            time.sleep(1)
    except KeyboardInterrupt:
        pass
    finally:
        destroyNetwork(peers)
