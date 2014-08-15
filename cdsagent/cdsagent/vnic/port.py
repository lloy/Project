import logging
from cdsagent import cfg
# from cdsagent.log import LOG
from cdsagent import utils

__author__ = 'Hardy.zheng'
__email__ = 'wei.zheng@yun-idc.com'


LOG = logging.getLogger(__name__)
conf = cfg.CONF


class BasePoller(object):

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
        self.rx = 'in'
        self.tx = 'out'
        self.setpoller()

    def set_api(self):
        namespace = conf.float_ip.name
        name = conf.float_ip.api
        mgr = utils.get_manager(namespace, name, load=True)
        return mgr.driver

    def set_fetcher(self):
        namespace = conf.fetch.name
        name = conf.fetch.src
        LOG.info('namespace :%s - name: %s' % (namespace, name))
        mgr = utils.get_manager(namespace, name, load=True)
        return mgr.driver

    def set_pusher(self):
        namespace = conf.push.name
        name = conf.push.dest
        mrg = utils.get_manager(namespace, name, load=True)
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
        return self.api.get_floating_ips()

    def clear(self):
        self.pusher.clear()

    def get_packet(self, ip, packets_set):
        rxs = {}
        txs = {}
        for count in packets_set:
            for inpacket in count[self.rx].split('\n'):
                if ip in inpacket:
                    self._count_packet(rxs, ip, inpacket, sign='rx')
                    break
            for outpacket in count[self.tx].split('\n'):
                if ip in outpacket:
                    self._count_packet(txs, ip, outpacket, sign='tx')
                    break
        if rxs and txs:
            return rxs['rpacket'], rxs['rbyte'], txs['tpacket'], txs['tbyte']
        elif rxs and not txs:
            return rxs['rpacket'], rxs['rbyte'], 0, 0
        elif not rxs and txs:
            return 0, 0, txs['tpacket'], txs['tbyte']
        else:
            return 0, 0, 0, 0

    def _count_packet(self, rtx, ip, packet, sign=None):
        ip, num, size = packet.split()
        if rtx.get(ip, None):
            if sign == 'rx':
                rtx[ip]['rpacket'] += int(num)
                rtx[ip]['rbyte'] += int(size)
            else:
                rtx[ip]['tpacket'] += int(num)
                rtx[ip]['tbyte'] += int(size)
        else:
            if sign == 'rx':
                rtx[ip] = {'rpacket': int(num), 'rbyte': int(size)}
            else:
                rtx[ip] = {'tpacket': int(num), 'tbyte': int(size)}

    def run(self):
        LOG.info('PortPoller starting ...')
        timestamp = utils.utcnow()
        LOG.info('PortPoller run() %s ...' % str(timestamp))
        try:
            rpacket = rbyte = tpacket = tbyte = None
            # ips = self.float_ips()
            packets = self.fetcher.fetch()
            # # for ip in ips:
                # # rpacket, rbyte, tpacket, tbyte = self.get_packet(ip, packets)
                # # q = {'uuid': ip.instance_id,
                     # # 'ip': ip.ip,
                     # # 'rpacket': rpacket,
                     # # 'tpacket': tpacket,
                     # # 'rbyte': rbyte,
                     # # 'tbyte': tbyte,
                     # # 'timestamp': timestamp
                     # # }

            q = {'test': 'Hardy.zheng'}
            LOG.info('pusher data %s' % str(q))
            self.pusher.push(q)
            # self.clear()
        except Exception, e:
            LOG.error('PortPoller Error: %s' % str(e))
