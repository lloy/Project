import logging
import copy
import traceback


from cdsagent import cfg
from cdsagent import utils
from cdsagent import exc

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
        try:
            super(PortPoller, self).__init__()
            self.sections = ['float_ip', 'fetcher', 'pusher']
            self.rx = 'in'
            self.tx = 'out'
        except Exception:
            raise

    def set_api(self):
        namespace = conf.float_ip.name
        name = conf.float_ip.api
        try:
            mgr = utils.get_manager(namespace, name, load=True)
            return mgr.driver
        except exc.NovaClientInitError, e:
            LOG.error('set api failed')
            raise e

    def set_fetcher(self):
        namespace = conf.fetch.name
        name = conf.fetch.src
        url = cfg.CONF.database.connection
        try:
            mgr = utils.get_manager(namespace, name, load=True, args=(url,))
            return mgr.driver
        except Exception, e:
            LOG.error('set fetcher failed')
            raise e

    def set_pusher(self):
        namespace = conf.push.name
        name = conf.push.dest
        try:
            mrg = utils.get_manager(namespace, name, load=True)
            return mrg.driver
        except Exception, e:
            LOG.error('set pusher failed')
            raise e

    def setpoller(self):
        try:
            self.api = self.set_api()
            self.fetcher = self.set_fetcher()
            self.pusher = self.set_pusher()
        except Exception, e:
            LOG.error(str(e))
            raise exc.SetPollerError('Set Poller Error')

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
        LOG.debug('get_packet call')
        LOG.debug('ip: %s' % ip)
        rxs = {'rpacket': 0, 'rbyte': 0}
        txs = {'tpacket': 0, 'tbyte': 0}
        for count in packets_set:
            # LOG.debug('count : %s' % str(count))

            # incoming traffic
            in_traffic = count.get(self.rx, None)
            if not in_traffic:
                continue
            # LOG.debug('in_traffic : %s' % in_traffic)
            for inpacket in in_traffic.split('\n'):
                if ip in inpacket:
                    LOG.debug('inpacket: %s' % inpacket)
                    LOG.debug('inpacket ipxxx : %s' % ip)
                    self._count_packet(rxs, inpacket, sign='rx')
                    break

            # output traffic
            out_traffic = count.get(self.tx, None)
            if not out_traffic:
                continue
            for outpacket in out_traffic.split('\n'):
                if ip in outpacket:
                    LOG.debug('outpacket: %s' % outpacket)
                    LOG.debug('outpacket ipxxx : %s' % ip)
                    self._count_packet(txs, outpacket, sign='tx')
                    break

        if rxs and txs:
            return rxs['rpacket'], rxs['rbyte'], txs['tpacket'], txs['tbyte']
        elif rxs and not txs:
            return rxs['rpacket'], rxs['rbyte'], 0, 0
        elif not rxs and txs:
            return 0, 0, txs['tpacket'], txs['tbyte']
        else:
            return 0, 0, 0, 0

    def _count_packet(self, rtx, packet, sign=None):
        ip, num, size = packet.split()
        LOG.debug('ip %s num %d size %d' % (ip, int(num), int(size)))
        if sign == 'rx':
            rtx['rpacket'] += int(num)
            rtx['rbyte'] += int(size)
        else:
            rtx['tpacket'] += int(num)
            rtx['tbyte'] += int(size)

    def run(self):
        LOG.info('PortPoller starting ...')
        timestamp = utils.utcnow()
        LOG.info('PortPoller run() %s ...' % str(timestamp))
        try:
            self.setpoller()
            rpacket = rbyte = tpacket = tbyte = None
            ips = self.float_ips()
            LOG.debug('Openstack floatting ips %s' % str(ips))
            packets = self.fetcher.fetch()
            if not packets:
                LOG.warning('not fetch net traffic')
                return
            for ip in ips:
                packet_copies = copy.copy(packets)
                rpacket, rbyte, tpacket, tbyte = self.get_packet(ip['ip'],
                                                                 packet_copies)
                q = {'instance_uuid': ip['instance_id'],
                     'ip': ip['ip'],
                     'rpackets': rpacket,
                     'tpackets': tpacket,
                     'rbytes': rbyte,
                     'tbytes': tbyte,
                     'insert_timestamp': timestamp
                     }
                LOG.info('pusher data %s' % str(q))
                self.pusher.push(**q)
                # self.clear()
        except Exception:
            exstr = traceback.format_exc()
            LOG.error('PortPoller Error: %s\n' % str(exstr))
