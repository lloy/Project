import datatime

from cdsagent.common.mysqldb import MysqlBase
from cdsagent import exc
from cdsagent.log import LOG
from cdsagent import cfg

__author__ = 'Hardy.zheng'


class MysqlPusher(MysqlBase):

    def __init__(self):
        super(MysqlPusher, self).__init__()

    def get_timestamp(self):
        pass

    def push(self):
        pass
