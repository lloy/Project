from cdsagent.log import LOG
from cdsagent import cfg


__author__ = 'Hardy.zheng'
conf = cfg.CONF


class ApiBase(object):

    def __init__(self):
        pass


class CdsApi(ApiBase):

    def __init__(self):
        super(CdsApi, self).__init__()

    def get_floating_ips(self):
        LOG.error('CdsApi:get_floating_ips not implement')
        raise NotImplementedError("Cdsapi get_floating_ips method \
                wasn't implement")
