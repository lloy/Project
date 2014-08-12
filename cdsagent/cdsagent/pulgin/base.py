from cdsagent.exc import NotImplementedError

__author__ = 'Hardy.zheng'


class Connection(object):

    def __init__(self, url):
        """Constructor."""
        pass

    @classmethod
    def get_rx_resources(self, ip):
        raise NotImplementedError('rx traffic not implemented')

    @classmethod
    def get_tx_resources(self, ip):
        raise NotImplementedError('tx traffic not implemented')
