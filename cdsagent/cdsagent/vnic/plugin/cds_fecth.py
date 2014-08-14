import datatime

from cdsagent.common.mongodb import MongoBase
from cdsagent import exc

__author__ = 'Hardy.zheng'


class MongoFetcher(MongoBase):

    def __init__(self, url):
        super(MongoFetcher, self).__init__(url)
        self.locker_sgin = 'Y'

    def set_lock(self):
        # get lock from table of processing
        locker = self.processing.find_one()
        lock = locker['processing']
        if lock == self.locker_sgin:
            return False
        else:
            q = {'_id': locker['_id'], 'processing': 'Y'}
            self.processing.save(q)
            return True

    def get_timestamp(self):
        stamp = self.db.stamp.find_one()
        if not stamp:
            return datatime.datatime.now().replace(second=0, microsecond=0)
        return stamp['last_process']

    def fetch(self):
        # to get last timestamp from table stamp where live in newlog datebase
        if not self.set_lock():
            raise exc.IsLock('already lock')
        timestamp = self.get_timestamp()
        packets = self.db.log.find({'stamp': {'$gt': timestamp}})
        if not packets:
            return None, None
        else:
            return packets['in'], packets['out']
