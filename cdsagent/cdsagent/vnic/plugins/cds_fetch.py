import datetime
import logging

from cdsagent.common.mongodb import MongoBase
from cdsagent import exc

__author__ = 'Hardy.zheng'


LOG = logging.getLogger(__name__)


class MongoFetcher(MongoBase):

    def __init__(self, url):
        super(MongoFetcher, self).__init__(url)
        self.locker_sign = 'Y'
        self.unlocker_sign = 'N'

    def set_lock(self):
        # get lock from table of processing
        locker = self.db.locker.find_one()
        LOG.debug('locker : %s' % str(locker))
        if not locker:
            self.db.locker.save({'lock': self.unlocker_sign})
            LOG.warning('processing table is empty, crated locker table')
            return True
        lock = locker['lock']
        if lock == self.locker_sign:
            return False
        else:
            q = {'_id': locker['_id'], 'processing': self.locker_sign}
            self.db.processing.save(q)
            return True

    def get_timestamp(self):
        stamp = self.db.timestamp.find_one()
        if not stamp:
            timestamp = datetime.datetime.now().replace(second=0, microsecond=0)
            self.db.timestamp.save({"last_stamp": timestamp})
            return timestamp
        return stamp['last_stamp']

    def fetch(self):
        LOG.info('MongoFetcher fetch')
        # to get last timestamp from table stamp where live in newlog datebase
        if not self.set_lock():
            raise exc.IsLock('already lock')
        timestamp = self.get_timestamp()
        packets = self.db.log.find({'stamp': {'$gt': timestamp}})
        if not packets:
            return None
        else:
            return packets
