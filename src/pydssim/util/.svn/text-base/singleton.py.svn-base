'''
Created on 24/08/2009

@author: LGustavo
'''

class singleton(type):

    def __init__(cls, name, base, dict):
        super(singleton, cls).__init__(name, base, dict)
        cls.__inst = None
        cls.__copy__ = lambda self: self
        cls.__deepcopy__ = lambda self, memo=None: self

    def __call__(cls, *args, **kw):
        if cls.__inst is None:
            cls.__inst = super(singleton, cls).__call__(*args, **kw)
        return cls.__inst