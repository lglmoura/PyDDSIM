'''
Created on 14/01/2010

@author: LGustavo
'''

import random

from zope.interface import implements
from twisted.internet import interfaces, reactor
from twisted.internet.protocol import Factory
from twisted.protocols.basic import LineReceiver

from twisted.internet.protocol import Protocol, ClientFactory
from twisted.internet import reactor
from sys import stdout

class Echo(Protocol):
    def dataReceived(self, data):
        stdout.write("Client %s"% data)
        self.transport.write("2")
 #s d sda 
class EchoClientFactory(ClientFactory):
    def startedConnecting(self, connector):
        print 'Client Started to connect.'
    
    def buildProtocol(self, addr):
        print 'Client Connected.'
        return Echo()
    
    def clientConnectionLost(self, connector, reason):
        print 'Client Lost connection.  Reason:', reason
    
    def clientConnectionFailed(self, connector, reason):
        print 'Client Connection failed. Reason:', reason


class Producer:
    """Send back the requested number of random integers to the client."""
    implements(interfaces.IPushProducer)
    def __init__(self, proto, cnt):
        self._proto = proto
        self._goal = cnt
        self._produced = 0
        self._paused = False
    def pauseProducing(self):
        """When we've produced data too fast, pauseProducing() will be
        called (reentrantly from within resumeProducing's transport.write
        method, most likely), so set a flag that causes production to pause
        temporarily."""
        self._paused = True
        print('pausing connection from %s' % (self._proto.transport.getPeer()))
    def resumeProducing(self):
        self._paused = False
        while not self._paused and self._produced < self._goal:
            next_int = random.randint(0, 10000)
            self._proto.transport.write('%d\r\n' % (next_int))
            self._produced += 1
            if self._produced == self._goal:
                self._proto.transport.unregisterProducer()
                self._proto.transport.loseConnection()
    def stopProducing(self):
        pass

class ServeRandom(LineReceiver):
    """Serve up random data."""
    def connectionMade(self):
        print('connection made from %s' % (self.transport.getPeer()))
        self.transport.write('how many random integers do you want?%s\r\n'% self.transport.getPeer())
    def lineReceived(self, line):
        cnt = line.strip()
        print 'entr %s' % (cnt)
        producer = Producer(self, cnt)
        self.transport.registerProducer(producer, True)
        producer.resumeProducing()
    def connectionLost(self, reason):
        print('connection lost from %s' % (self.transport.getPeer()))

port =1234
print "-----------------Server --------------------" 
for i in range(0,9):
    factory = Factory()
    
    factory.protocol = ServeRandom
    reactor.listenTCP(port, factory)
    
    print 'listening on %s...'%port
    port+=1
   
#reactor.run()

print "-----------------Client--------------------"

port = 1234
host = "localhost"
for i in range(0,9):
    reactor.connectTCP(host, port, EchoClientFactory())
    port+=1

reactor.run()
