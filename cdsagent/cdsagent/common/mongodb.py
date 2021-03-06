import pymongo
import weakref
import time
import logging

from cdsagent import utils
# from cdsagent import exc


__author__ = 'Hardy.zheng'

_RETRY_INTERVAL = 10
_MAX_RETRIES = 2
LOG = logging.getLogger(__name__)


class ConnectionPool(object):

    def __init__(self):
        self._pool = {}

    def connect(self, url):
        connection_options = pymongo.uri_parser.parse_uri(url)
        del connection_options['database']
        del connection_options['username']
        del connection_options['password']
        del connection_options['collection']
        pool_key = tuple(connection_options)

        if pool_key in self._pool:
            client = self._pool.get(pool_key)()
            if client:
                return client
        scheme = utils.urlsplit(url)
        log_data = {'db': scheme,
                    'nodelist': connection_options['nodelist']}
        LOG.info('Connecting to %(db)s on %(nodelist)s' % log_data)
        client = self._mongo_connect(url)
        self._pool[pool_key] = weakref.ref(client)
        return client

    @staticmethod
    def _mongo_connect(url):
        max_retries = _MAX_RETRIES
        retry_interval = _RETRY_INTERVAL
        attempts = 0
        while True:
            try:
                client = pymongo.MongoClient(url)
            except pymongo.errors.ConnectionFailure as e:
                if max_retries >= 0 and attempts >= max_retries:
                    LOG.error('Unable to connect to the database after '
                              '%(retries)d retries. Giving up.' %
                              {'retries': max_retries})
                    raise
                LOG.warning('Unable to connect to the database server: '
                            '%(errmsg)s. Trying again in %(retry_interval)d '
                            'seconds.' %
                            {'errmsg': e, 'retry_interval': retry_interval})
                attempts += 1
                time.sleep(retry_interval)
            else:
                return client


class MongoBase(object):

    CONNECTION_POOL = ConnectionPool()

    def __init__(self, url):

        self.conn = self.CONNECTION_POOL.connect(url)
        connection_options = pymongo.uri_parser.parse_uri(url)
        self.db = getattr(self.conn, connection_options['database'])
        if connection_options.get('username'):
            self.db.authenticate(connection_options['username'],
                                 connection_options['password'])

    def clear(self):
        self.conn.drop_database(self.db)
        # Connection will be reopened automatically if needed
        self.conn.close()

    def collections(self):
        self.db.collection_names()
