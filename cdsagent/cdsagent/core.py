from cdsagent import service as os_service
# from cdsagent import cfg
# from cdsagent import log
from cdsagent.agent import agentManager


__author__ = 'Hardy.zheng'

# def prepare_service(argv=None):


def run():
    os_service.launch(agentManager()).wait
