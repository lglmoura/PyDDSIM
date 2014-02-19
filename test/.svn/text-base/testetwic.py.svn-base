'''
Created on 14/01/2010

@author: LGustavo
'''
from twisted.internet.protocol import Protocol, ClientFactory
from twisted.internet import reactor
from sys import stdout

class Echo(Protocol):
    def dataReceived(self, data):
        stdout.write("Client %s"% data)

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


port = 1234
host = "localhost"
for i in range(0,9):
    reactor.connectTCP(host, port, EchoClientFactory())
    port+=1

reactor.run()
