from cdsagent.log import LOG
from cdsagent import cfg
from cdsagent import exc
from cdsagent import service as os_service
from cdsagent import utils

__author__ = 'Hardy.zheng'


_TASKS = ['nic', 'disk', ]


class AgentManager(os_service.Service):

    def __init__(self):
        super(AgentManager, self).__init__()

    def start(self):
        LOG.info('start cdsagent....')
        for task in _TASKS:
            print cfg.CONF.log.level
            worker = getattr(cfg.CONF, task, None)
            if not worker:
                continue
            if not hasattr(worker, 'poller'):
                raise exc.NotSetPoller('not set poller in \
                    section configure file')
            poller = worker.poller
            mgr = utils.get_manager(task, poller, False)

            if not hasattr(mgr.driver, 'run'):
                raise exc.NotRunMethod('Not Found run() \
                        method in %s Poller' % task, '0000-003-01')

            interval = int(worker.interval)
            LOG.info('type: %s, interval:%d' % (task, interval))
            self.tg.add_timer(interval,
                              self.interval_task,
                              task=mgr.driver().run)

    @staticmethod
    def interval_task(task):
        try:
            task()
        except Exception, e:
            LOG.error(str(e))
