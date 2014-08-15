
import logging
from cdsagent import cfg

LOG = logging.getLogger(__name__)


__author__ = 'Hardy.zheng'
conf = cfg.CONF


class ApiBase(object):

    def __init__(self):
        pass


class CdsClient(ApiBase):

    def __init__(self):
        super(CdsClient, self).__init__()

    def get_floating_ips(self):
        LOG.error('CdsClient:get_floating_ips not implement')
        raise NotImplementedError("CdsClient get_floating_ips method \
                wasn't implement")
