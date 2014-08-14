
import MySQLdb

from cdsagent.common import base
from cdsagent import cfg
from cdsagent.log import LOG


__author__ = 'Hardy.zheng'

conf = cfg.CONF


class MysqlBase(base.Connection):
    def __init__(self, dbname):
        try:
            self.conn = MySQLdb.connect(host=conf.mysql.host,
                                        user=conf.mysql.user,
                                        passwd=conf.mysql.passwd,
                                        db=dbname,
                                        port=int(conf.mysql.port))
        except MySQLdb.Error, e:
            self.conn = None
            LOG.error(str(e))

    def clear(self):
        self.conn.close()
