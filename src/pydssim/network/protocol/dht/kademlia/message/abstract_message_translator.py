'''
Created on 21/12/2009

@author: LGustavo
'''
from pydssim.network.protocol.dht.kademlia.message.i_message_translator import IMessageTranslator
from pydssim.network.protocol.dht.kademlia.message.request_message import RequestMessage
from pydssim.network.protocol.dht.kademlia.message.response_message import ResponseMessage
from pydssim.network.protocol.dht.kademlia.message.error_message import ErrorMessage

class AbstractMessageTranslator(IMessageTranslator):
    """ The default on-the-wire message format for this library """
    typeRequest, typeResponse, typeError = range(3)
    headerType, headerMsgID, headerNodeID, headerPayload, headerArgs = range(5)
    
    def fromPrimitive(self, msgPrimitive):
        
        msgType = msgPrimitive[self.headerType]
       
        if msgType == self.typeRequest:
            msg = RequestMessage(msgPrimitive[self.headerNodeID], msgPrimitive[self.headerPayload], msgPrimitive[self.headerArgs], msgPrimitive[self.headerMsgID])
        elif msgType == self.typeResponse:
            msg = ResponseMessage(msgPrimitive[self.headerMsgID], msgPrimitive[self.headerNodeID], msgPrimitive[self.headerPayload])
        elif msgType == self.typeError:
            msg = ErrorMessage(msgPrimitive[self.headerMsgID], msgPrimitive[self.headerNodeID], msgPrimitive[self.headerPayload], msgPrimitive[self.headerArgs])
        else:
            # Unknown message, no payload
            msg = Message(msgPrimitive[self.headerMsgID], msgPrimitive[self.headerNodeID])
        return msg
    
    def toPrimitive(self, message):    
        msg = {self.headerMsgID:  message.id,
               self.headerNodeID: message.peerID}
        if isinstance(message, RequestMessage):
            msg[self.headerType] = self.typeRequest
            msg[self.headerPayload] = message.request
            msg[self.headerArgs] = message.args
        elif isinstance(message, ErrorMessage):
            msg[self.headerType] = self.typeError
            msg[self.headerPayload] = message.exceptionType
            msg[self.headerArgs] = message.response
        elif isinstance(message, ResponseMessage):
            msg[self.headerType] = self.typeResponse
            msg[self.headerPayload] = message.response
        return msg
