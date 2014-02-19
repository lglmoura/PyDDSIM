'''
Created on 22/08/2009

@author: LGustavo
'''
from datetime import datetime

import locale
import os
from threading import Semaphore
from pydssim.util.singleton import singleton


class AbstractLogger():
    '''
    Class for logging
    line = str(priority) + " " + opportunityId + " " + self.getId() + " " + str(deviceType) + " " +  str(capacity)
        messagesLogFile.write(str(line)+"\n")
        messagesLogFile.close() 
     
    '''
         
    __metaclass__ = singleton    
    
    def __init__(self):
       
        raise NotImplementedError()
        
    
    def initialize(self,fileMode="a",logFileName="log.log"):
        
        
        
        self.debug = False
        
        '''
        name,ext = logFileName.split(".")
    
        hoje = datetime.today()
        dia = hoje.strftime('%d%m%Y-%I%M%S')
        logFileName = "%s-%s.%s"%(name,dia,ext)
        '''
        
        self.__messagesLogFile = self.openFileLog(logFileName, fileMode)
            
        
   
   
    def createMessage(self,level,msg1):
        format='%a, %d-%b-%Y %H:%M:%S %p'
        
        locale.setlocale(locale.LC_ALL, '')


        hoje = datetime.today()
        agora = hoje.strftime(format)
        msg = "%s- %s - %s"%(agora,level,msg1)
        return msg
        
        
    def resgiterLoggingInfo(self, msg):
        #self.logger.info(msg)
        msg = self.createMessage("INFO", msg)
        self.__messagesLogFile.write( msg+"\n")
        #self.__messagesLogFile.close()
        if self.debug:
            print msg     
    
    
    def resgiterLoggingError(self, msg):
        msg = self.createMessage("DEBUG", msg)
        self.__messagesLogFile.write( msg+"\n")
        
        if self.debug:
            print msg
            
    def openFileLog(self,nameFile,fileMode):
                       
        return open(nameFile, fileMode)
        
        
