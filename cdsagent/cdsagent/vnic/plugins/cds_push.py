import logging
from MySQLdb import Error as MySqlError

from cdsagent.common.mysqldb import MysqlBase
# from cdsagent.log import LOG
from cdsagent import cfg

__author__ = 'Hardy.zheng'

conf = cfg.CONF
LOG = logging.getLogger(__name__)


class MysqlPusher():

    def __init__(self):
        LOG.info('MysqlPusher init')

    def clear(self):
        LOG.info('MysqlPusher.clear() call')

    def push(self, q):
        LOG.info('MysqlPusher.push() %s ' % str(q))


# class MysqlPusher(MysqlBase):

    # def __init__(self):
        # dbname = conf.mysql.dbname
        # super(MysqlPusher, self).__init__(dbname)
        # self.table = conf.mysql.table
        # self.cur = self.conn.cursor()

    # def clear(self):
        # try:
            # self.conn.close()
            # self.cur.close()
        # except MySqlError, e:
            # LOG.error(str(e))

    # def push(self, **q):
        # try:
            # if not self.conn and not self.cur:
                # raise MySqlError('Not connect Mysql')
            # command = "insert into %s values(%s,%s,%s,%s,%s,%s,%s)" \
                      # % (self.table,
                         # q['uuid'],
                         # q['ip'],
                         # q['rpacket'],
                         # q['rbyte'],
                         # q['tpacket'],
                         # q['tbyte'],
                         # q['timestamp'])
            # self.cur.execute(command)
            # self.conn.commit()
        # except Exception, e:
            # LOG.error('MysqlPusher push error')
            # raise MySqlError(str(e))
