'''
Created on 22/08/2009

@author: LGustavo
'''



def implements(obj, *interfaces):
    """Returns 1 if obj implements *all* interfaces, 0 otherwise."""
    for interface in interfaces:
        if not interface.implements(obj):
            return 0
    return 1


def return_type(type):
    def make_wrapper(f):
        def wrapper(*args, **kwargs):
            obj = f(*args, **kwargs)
            if obj:
                if hasattr(type, "implements"):
                    if not implements(obj, type):
                        raise TypeError, "Expected '%s' ; was %s." % (type, obj.__class__)
                elif not isinstance(obj, type):
                    raise TypeError, "Expected '%s' ; was %s." % (type, obj.__class__)
            return obj
        return wrapper
    return make_wrapper