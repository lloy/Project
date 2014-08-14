from cdsagent.log import LOG
from novaclient.v1_1 import client as nova_client
from cdsagent import cfg
from cdsagent import exc


__author__ = 'Hardy.zheng'
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


class NovaClient(object):

    def __init__(self):
        LOG.info('NovaClient call')

    def get_floating_ips(self):
        LOG.info('NovaClient.get_floating_ips() call')

# class NovaClient(OpenstackClientBase):

    # def __init__(self):
        # super(NovaClient, self).__init__()
        # self.set_service_type('compute')
        # self.client = nova_client.Client(**self.keystone)

    # def get_floating_ips(self):
        # try:
            # ips = []
            # for ip in self.nova.floating_ips.list(self.search_opts):
                # d = {}
                # d['instance_id'] = ip.instance_id
                # d['ip'] = ip.ip
                # ips.append(d)
            # return ips
        # except Exception, e:
            # LOG.error(str(e))
            # raise exc.RunNovaClientError('nova client not process')


class CeilometerClient(OpenstackClientBase):

    def __init__(self):
        raise NotImplementedError('CeilometerClient not Implemented')
