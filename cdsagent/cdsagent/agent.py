from stevedore import driver
from cdsagent.log import LOG
from cdsagent import cfg
from cdsagent import exc
from cdsagent import service as os_service

__author__ = 'Hardy.zheng'


_TASKS = ['nic', 'disk', ]


class AgentManager(os_service.Service):

    def __init__(self):
        super(AgentManager, self).__init__()

    def get_manager(slef, namespace, name, load=True, args=()):
        LOG.info('namespace: %s -->  name: %s' % (namespace, name))
        return driver.DriverManager(
            namespace=namespace,
            name=name,
            invoke_on_load=True,
            invoke_args=())

    def start(self):
        LOG.info('zhengwei 0')
        for task in _TASKS:
            worker = getattr(cfg.CONF, task, None)
            if not worker:
                continue
            if not hasattr(worker, 'poller'):
                raise exc.NotSetPoller('not set poller in section %s configure file' % t, '0000-001-02')
            poller = worker.poller
            LOG.info('poller %s' % poller)
            mgr = self.get_manager(task, poller, False)
            LOG.info('zhengwei 1')

            if not hasattr(mgr.driver, 'run'):
                LOG.info('zhengwei 3')
                raise exc.NotRunMethod('Not Found run() method in %s Poller' % task, '0000-003-01')

            LOG.info('zhengwei 4')
            interval = int(worker.interval)
            LOG.info('type: %s, interval:%d' % (task, interval))

            LOG.info('zhengwei mgr')
            self.tg.add_timer(interval,
                              self.interval_task,
                              task=mgr.driver.run)

    @staticmethod
    def interval_task(task):
        try:
            # LOG.info(task)
            task()
        except Exception, e:
            LOG.error(str(e))
