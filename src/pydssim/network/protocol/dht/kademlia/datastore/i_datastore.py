'''
Created on 19/12/2009

@author: LGustavo
'''

import UserDict



class IDataStore(UserDict.DictMixin):
    """ Interface for classes implementing physical storage (for data
    published via the "STORE" RPC) for the Kademlia DHT
    
    @note: This provides an interface for a dict-like object
    """
    def keys(self):
        """ Return a list of the keys in this data store """

    def lastPublished(self, key):
        """ Get the time the C{(key, value)} pair identified by C{key}
        was last published """

    def originalPublisherID(self, key):
        """ Get the original publisher of the data's node ID

        @param key: The key that identifies the stored data
        @type key: str

        @return: Return the node ID of the original publisher of the
        C{(key, value)} pair identified by C{key}.
        """

    def originalPublishTime(self, key):
        """ Get the time the C{(key, value)} pair identified by C{key}
        was originally published """

    def setItem(self, key, value, lastPublished, originallyPublished, originalPublisherID):
        """ Set the value of the (key, value) pair identified by C{key};
        this should set the "last published" value for the (key, value)
        pair to the current time
        """

    def __getitem__(self, key):
        """ Get the value identified by C{key} """

    def __setitem__(self, key, value):
        """ Convenience wrapper to C{setItem}; this accepts a tuple in the
        format: (value, lastPublished, originallyPublished, originalPublisherID) """
        self.setItem(key, *value)

    def __delitem__(self, key):
        """ Delete the specified key (and its value) """