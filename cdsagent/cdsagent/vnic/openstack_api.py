import logging

from novaclient.v1_1 import client as nova_client
from cdsagent import cfg
from cdsagent import exc


__author__ = 'Hardy.zheng'

LOG = logging.getLogger(__name__)
conf = cfg.CONF


class OpenstackClientBase(object):

    def __init__(self):
        self.keystone = {'username': conf.keystone.os_username,
                         'api_key': conf.keystone.os_password,
                         'project_id': conf.keystone.os_tenant_name,
                         'auth_url': conf.keystone.os_auth_url,
                         'no_cache': True}
        self.search_opts = {'all_tenants': True}

    def set_service_type(self, service_type):
        self.keystone.update(service_type=service_type)


class NovaClient(OpenstackClientBase):

    def __init__(self):
        super(NovaClient, self).__init__()
        self.set_service_type('compute')
        try:
            self.nova = nova_client.Client(**self.keystone)
        except Exception, e:
            LOG.error(str(e))
            raise exc.NovaClientInitError('NovaClient Init Error')

    def get_floating_ips(self):
        try:
            ips = []
            for ip in self.nova.floating_ips.list(self.search_opts):
                d = {}
                if not ip.instance_id:
                    continue
                d['instance_id'] = ip.instance_id
                d['ip'] = ip.ip
                ips.append(d)
            return ips
        except Exception, e:
            LOG.error(str(e))
            raise exc.RunNovaClientError('get floating ip across NovaClient Error')


class CeilometerClient(OpenstackClientBase):

    def __init__(self):
        raise NotImplementedError('CeilometerClient not Implemented')
