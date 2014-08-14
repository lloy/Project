
from cdsagent import cfg
from cdsagent.log import LOG
from cdsagent import utils

__author__ = 'Hardy.zheng'
__email__ = 'wei.zheng@yun-idc.com'

conf = cfg.CONF


def _setapi():
    namespace = conf.float_ip.name
    name = conf.float_ip.api
    return utils.get_manager(namespace, name, load=True, args=())


def BasePoller(object):

    def __init__(self):
        self.api = None
        self.fetcher = None
        self.pusher = None

    def set_api(self):
        pass

    def set_fetcher(self):
        pass

    def set_pusher(self):
        pass

    def run(self):
        pass


class PortPoller(BasePoller):

    def __init__(self):
        super(PortPoller, self).__init__()
        self.sections = ['float_ip', 'fetcher', 'pusher']
        self.setpoller()

    def set_api(self):
        namespace = conf.float_ip.name
        name = conf.float_ip.api
        mgr = utils.get_manager(namespace, name, load=True, args=())
        return mgr.driver

    def set_fetcher(self):
        namespace = conf.fetch.name
        name = conf.fetch.src
        mgr = utils.get_manager(namespace, name, load=True, args=())
        return mgr.driver

    def set_pusher(self):
        namespace = conf.pusher.name
        name = conf.pusher.dest
        mrg = utils.get_manager(namespace, name, load=True, args=())
        return mrg.driver

    def setpoller(self):
        self.api = self.set_api()
        self.fetcher = self.set_fetcher()
        self.pusher = self.set_pusher()

    def float_ips(self):
        """
        return value :
        [
            {'instance_id':dda53916-40ad-49c5-b30d-dbcd5e7fab73,
             'ip':'202.78.9.107'},
            {'instance_id':dda53916-41ad-49c5-b30d-dbcd5e7fab73,
            'ip':'202.78.9.117'},...]
        """
        return self.api.driver.get_floating_ips()

    def clear(self):
        pass

    def run(self):
        LOG.info('PortPoller starting ...')
        timestamp = utils.utcnow()
        try:
            rpacket = rbyte = tpacket = tbyte = None
            ips = self.float_ips()
            rxs, txs = self.fetcher.fetch()
            for ip in ips:
                for rx in rxs:
                    if ip.ip in rx:
                        ip, rpacket, rbyte = rx.split()
                        break
                for tx in txs:
                    if ip.ip in tx:
                        ip, tpacket, tbyte = tx.split()
                        break
                q = {'uuid': ip.instance_id,
                     'ip': ip.ip,
                     'rpacket': rpacket,
                     'tpacket': tpacket,
                     'rbyte': rbyte,
                     'tbyte': tbyte,
                     'timestamp': timestamp
                     }
                LOG.info('pusher data %s' % str(q))
                self.pusher.push(q)
            self.clear()
        except Exception, e:
            LOG.error('PortPoller Error: %s' % str(e))
