# from cdsagent.log import LOG
import logging


LOG = logging.getLogger(__name__)

__author__ = 'Hardy.zheng'


class DiskPoller(object):

    def __init__(self):
        pass

    def run(self):
        LOG.info('DiskPoller start...')
