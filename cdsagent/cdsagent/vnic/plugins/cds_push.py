import logging
from MySQLdb import Error as MySqlError

from cdsagent.common.mysqldb import MysqlBase
from cdsagent import cfg

__author__ = 'Hardy.zheng'

conf = cfg.CONF
LOG = logging.getLogger(__name__)


class MysqlPusher(MysqlBase):

    def __init__(self):
        dbname = conf.mysql.dbname
        super(MysqlPusher, self).__init__(dbname)
        self.table = conf.mysql.table
        self.cur = self.conn.cursor()

    def clear(self):
        try:
            self.conn.close()
            self.cur.close()
        except MySqlError, e:
            LOG.error(str(e))

    def push(self, **q):
        try:
            if not self.conn and not self.cur:
                raise MySqlError('Not connect Mysql')
            command = "insert into %s (instance_uuid,\
                                       ip,\
                                       rpackets,\
                                       rbytes,\
                                       tpackets,\
                                       tbytes,\
                                       inster_timestamp)\
                                    values('%s','%s',%s,%s,%s,%s,'%s')" \
                      % (self.table,
                         str(q['instance_uuid']),
                         str(q['ip']),
                         q['rpackets'],
                         q['rbytes'],
                         q['tpackets'],
                         q['tbytes'],
                         q['insert_timestamp'])

            LOG.debug('insert command %s' % command)
            self.cur.execute(command)
            self.conn.commit()
        except Exception, e:
            LOG.error('MysqlPusher push error')
            raise MySqlError(str(e))
