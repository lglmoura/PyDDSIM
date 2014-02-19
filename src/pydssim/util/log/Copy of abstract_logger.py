'''
Created on 22/08/2009

@author: LGustavo
'''

from datetime import datetime
import logging


class AbstractLogger():
    '''
    Class for logging
    line = str(priority) + " " + opportunityId + " " + self.getId() + " " + str(deviceType) + " " +  str(capacity)
        messagesLogFile.write(str(line)+"\n")
        messagesLogFile.close() 
     
    '''
        
    
    def __init__(self):
        
        raise NotImplementedError()
        
    
    def initialize(self,fileMode="w",logFileName="log.log"):
        
        self.debug = False
        self.__messagesLogFile = self.openFileLog(logFileName, fileMode)
        #today = datetime.today().strftime("%Y_%m_%d_%H_%M_%S")
        #LOG_FILENAME = 'logging_simulatorfile_'+today+'.log'
        
        LOG_FILENAME = logFileName
        logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    datefmt='%a, %d %b %Y %H:%M:%S',
                    filename=LOG_FILENAME,
                    filemode=fileMode)
        self.logger = logging.getLogger("pydssim")
        
   
    def resgiterLoggingInfo(self, msg):
        self.logger.info(msg)
        if self.debug:
            print msg     
    
    
    def resgiterLoggingError(self, msg):
        self.logger.error(msg)
        if self.debug:
            print msg
            
    def openFileLog(self,nameFile,fileMode):
        
        messagesLogFile = open(nameFile, fileMode)
        
        
