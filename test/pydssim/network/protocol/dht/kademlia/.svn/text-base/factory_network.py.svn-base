#!/usr/bin/env python
#
# This library is free software, distributed under the terms of
# the GNU Lesser General Public License Version 3, or any later version.
# See the COPYING file included in this archive
#

# Thanks to Paul Cannon for IP-address resolution functions (taken from aspn.activestate.com)

import os, sys, time, signal
from pydssim.network.protocol.dht.dht_peer import DHTPeer


import twisted.internet.reactor

def destroyNetwork(peers):
    pass


def createPeer(port=4000,ipaddress=None,startport=None):
    #import twisted.internet.reactor
    import sys, os

    if ipaddress != None:
        knownPeers = [(ipaddress, startport)]
        
    else:
        knownPeers = None

    #print knownPeers, port
    peer = DHTPeer(udpPort=port)
    
    peer.joinNetwork(knownPeers)
    #peer.printNeighbors()
    #print port,ipaddress,startPort
    return peer
    

if __name__ == '__main__':
   
    amount = 30 #int(sys.argv[1])
    import socket
    ipAddress = socket.gethostbyname(socket.gethostname())
    print 'Network interface IP address omitted; using %s   ...' % ipAddress
    
    startPort = 4000
    port = startPort+1
    peers = []
    print 'Creating Kademlia network...'
    try:
        
        createPeer(startPort)
        
        for i in range(amount-1):
            time.sleep(0.15)
            hashAmount = i*50/amount
            hashbar = '#'*hashAmount
            output = '\r[%-50s] %d/%d %s\n' % (hashbar, i, amount-1,port)
            sys.stdout.write(output)
           
            peer = createPeer(port,ipAddress,startPort)
            peers.append(peer)
            #peer.printNeighbors()
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
