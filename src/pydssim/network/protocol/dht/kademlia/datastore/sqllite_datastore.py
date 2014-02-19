'''
Created on 19/12/2009

@author: LGustavo
'''
import sqlite3
import cPickle as pickle
import time
import os

from pydssim.network.protocol.dht.kademlia.datastore.i_datastore import IDataStore

class SQLLiteDataStore(IDataStore):
    """ Example of a SQLite database-based datastore
    """
    def __init__(self, dbFile=':memory:'):
        """
        @param dbFile: The name of the file containing the SQLite database; if
                       unspecified, an in-memory database is used.
        @type dbFile: str
        """
        createDB = not os.path.exists(dbFile)
        self._db = sqlite3.connect(dbFile)
        self._db.isolation_level = None
        self._db.text_factory = str
        if createDB:
            self._db.execute('CREATE TABLE data(key, value, lastPublished, originallyPublished, originalPublisherID)')
        self._cursor = self._db.cursor()

    def keys(self):
        """ Return a list of the keys in this data store """
        keys = []
        try:
            self._cursor.execute("SELECT key FROM data")
            for row in self._cursor:
                keys.append(row[0].decode('hex'))
        finally:
            return keys

    def lastPublished(self, key):
        """ Get the time the C{(key, value)} pair identified by C{key}
        was last published """
        return int(self._dbQuery(key, 'lastPublished'))

    def originalPublisherID(self, key):
        """ Get the original publisher of the data's peer ID

        @param key: The key that identifies the stored data
        @type key: str
        
        @return: Return the peer ID of the original publisher of the
        C{(key, value)} pair identified by C{key}.
        """
        return self._dbQuery(key, 'originalPublisherID')

    def originalPublishTime(self, key):
        """ Get the time the C{(key, value)} pair identified by C{key}
        was originally published """
        return int(self._dbQuery(key, 'originallyPublished'))

    def setItem(self, key, value, lastPublished, originallyPublished, originalPublisherID):
        # Encode the key so that it doesn't corrupt the database
        encodedKey = key.encode('hex')
        self._cursor.execute("select key from data where key=:reqKey", {'reqKey': encodedKey})
        if self._cursor.fetchone() == None:
            self._cursor.execute('INSERT INTO data(key, value, lastPublished, originallyPublished, originalPublisherID) VALUES (?, ?, ?, ?, ?)', (encodedKey, buffer(pickle.dumps(value, pickle.HIGHEST_PROTOCOL)), lastPublished, originallyPublished, originalPublisherID))
        else:
            self._cursor.execute('UPDATE data SET value=?, lastPublished=?, originallyPublished=?, originalPublisherID=? WHERE key=?', (buffer(pickle.dumps(value, pickle.HIGHEST_PROTOCOL)), lastPublished, originallyPublished, originalPublisherID, encodedKey))
        
    def _dbQuery(self, key, columnName, unpickle=False):
        try:
            self._cursor.execute("SELECT %s FROM data WHERE key=:reqKey" % columnName, {'reqKey': key.encode('hex')})
            row = self._cursor.fetchone()
            value = str(row[0])
        except TypeError:
            raise KeyError, key
        else:
            if unpickle:
                return pickle.loads(value)
            else:
                return value

    def __getitem__(self, key):
        return self._dbQuery(key, 'value', unpickle=True)

    def __delitem__(self, key):
        self._cursor.execute("DELETE FROM data WHERE key=:reqKey", {'reqKey': key.encode('hex')})
