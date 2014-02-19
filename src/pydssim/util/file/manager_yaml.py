'''
Created on 11/09/2009

@author: LGustavo
'''

from pydssim.util.protected import Protected
from pydssim.util.decorator.public import public
from pydssim.util.logger import Logger
import yaml

class FileYaml(Protected):
    '''
    classdocs
    '''


    def __init__(self,fileName='network.yaml',method='r'):
        '''
        Constructor
        '''
        self.__fileName = fileName
        self.__method   = method
        
    
    @public
    def getContentFile(self):
        conf = open(self.__fileName, self.__method)
        params = yaml.load(conf)
        conf.close()
        Logger().resgiterLoggingInfo("Read Yaml file : "+self.__fileName )
        return params
        