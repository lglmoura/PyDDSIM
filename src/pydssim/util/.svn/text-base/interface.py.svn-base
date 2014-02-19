class Interface(type):

    def __init__(cls, name, bases, dct):
        super(Interface, cls).__init__(name, bases, dct)
        attribs = dct.keys()
        attribs.remove('__metaclass__')
        super(Interface, cls).__setattr__('__attributes__', attribs)

    #interfaces are "static" objects => we disallow dynamic changes.
    def __setattr__(self, name, value):
        raise AttributeError("Cannot bind attributes in interface classes.")

    def __delattr__(self, name):
        raise AttributeError("Cannot delete attributes in interface classes.")

    def attributes(self):
        """Returns the list of noncallable attributes's names."""
        #Get mro list of interfaces.
        interfaces = [interface for interface in self.mro() \
                      if isinstance(interface, Interface)]
        #Build list of attribs.
        attribs = {}
        for interface in interfaces:
            for attrib in interface.__attributes__:
                if not callable(getattr(interface, attrib)):
                    attribs[attrib] = None
        return attribs.keys()

    def callables(self):
        """Returns the list of callable attributes's names."""
        #Get mro list of interfaces.
        interfaces = [interface for interface in self.mro() \
                      if isinstance(interface, Interface)]
        #Build list of attribs.
        attribs = {}
        for interface in interfaces:
            for attrib in interface.__attributes__:
                if callable(getattr(interface, attrib)):
                    attribs[attrib] = None
        return attribs.keys()

    def implements(self, obj):
        """Returns 1 if obj implements interface cls, 0 otherwise."""
        #Check attributes.
        for attrib in self.attributes():
            try:
                objattrib = getattr(obj, attrib)
            except AttributeError, e:
                print 11111111111111111111111111111111111
                print e
                return 0
            else:
                if callable(objattrib):
                    print objattrib
                    return 0
        #Check callables.
        for attrib in self.callables():
            try:
                objattrib = getattr(obj, attrib)
            except AttributeError, e:
                print e
                return 0
            else:
                if not callable(objattrib):
                    return 0
        return 1


def implements(obj, *interfaces):
    """Returns 1 if obj implements *all* interfaces, 0 otherwise."""
    for interface in interfaces:
        if not interface.implements(obj):
            return 0
    return 1



