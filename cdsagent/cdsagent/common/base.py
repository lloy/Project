__author__ = 'Hardy.zheng'


class Connection(object):

    def __init__(self):
        """Constructor."""
        pass

    def get_rx_resources(self, ip):
        raise NotImplementedError('rx traffic not implemented')

    def get_tx_resources(self, ip):
        raise NotImplementedError('tx traffic not implemented')
