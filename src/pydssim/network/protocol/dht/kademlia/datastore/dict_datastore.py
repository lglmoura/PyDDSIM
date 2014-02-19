'''
Created on 19/07/2009

@author: LGustavo
'''

from pydssim.network.protocol.dht.kademlia.datastore.i_datastore import IDataStore

class DictDataStore(IDataStore):
    """ A datastore using an in-memory Python dictionary """
    def __init__(self):
        # Dictionary format:
        # { <key>: (<value>, <lastPublished>, <originallyPublished> <originalPublisherID>) }
        self._dict = {}

    def keys(self):
        """ Return a list of the keys in this data store """
        return self._dict.keys()

    def lastPublished(self, key):
        """ Get the time the C{(key, value)} pair identified by C{key}
        was last published """
        return self._dict[key][1]

    def originalPublisherID(self, key):
        """ Get the original publisher of the data's node ID
        
        @param key: The key that identifies the stored data
        @type key: str
        
        @return: Return the node ID of the original publisher of the
        C{(key, value)} pair identified by C{key}.
        """
        return self._dict[key][3]

    def originalPublishTime(self, key):
        """ Get the time the C{(key, value)} pair identified by C{key}
        was originally published """
        return self._dict[key][2]

    def setItem(self, key, value, lastPublished, originallyPublished, originalPublisherID):
        """ Set the value of the (key, value) pair identified by C{key};
        this should set the "last published" value for the (key, value)
        pair to the current time
        """
        self._dict[key] = (value, lastPublished, originallyPublished, originalPublisherID)

    def __getitem__(self, key):
        """ Get the value identified by C{key} """
        return self._dict[key][0]

    def __delitem__(self, key):
        """ Delete the specified key (and its value) """
        del self._dict[key]
