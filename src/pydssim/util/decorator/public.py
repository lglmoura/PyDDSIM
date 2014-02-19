'''
Created on 22/08/2009

@author: LGustavo
'''

import uuid



def public(f):
    '''
    Decorator used to assign the attribute __public__ to methods.
    '''
    f.__public__ = True
    return f


def createURN(type):
    
    '''
    Create URN.
    '''
    
    
   
    urn = "urn:"+type+":"+uuid.uuid1().__str__()
    return urn
