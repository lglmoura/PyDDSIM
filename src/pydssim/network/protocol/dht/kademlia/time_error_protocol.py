'''
Created on 21/08/2009

@author: LGustavo
'''
import time


class TimeoutErrorProtocol(Exception):
    """ Raised when a RPC times out """