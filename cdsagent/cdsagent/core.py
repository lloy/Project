from cdsagent import service as os_service
# from cdsagent import cfg
from cdsagent.log import LOG
from cdsagent.agent import AgentManager


__author__ = 'Hardy.zheng'

# def prepare_service(argv=None):


def run():
    os_service.launch(AgentManager()).wait()

if __name__ == '__main__':

    LOG.info('start cdsagent....')
    run()
