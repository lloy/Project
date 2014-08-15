
import ConfigParser
import os

from cdsagent import exc

__author__ = 'Hardy.zheng'


# _configure_file = './cds.cfg'
_configure_file = '/etc/cds/cds.cfg'

_DEFAULT_CONFIG = {
    'core': {
        'interval': 600},
    'database': {
        'connection': None},
    'mysql': {
        'host': 'localhost',
        'user': 'admin',
        'passwd': '12345',
        'port': '3306',
        'dbname': 'open_cloudoss',
        'table': 'flow_measure'},
    'keystone': {
        'os_auth_url': 'http://controller:5000/v2.0',
        'os_username': 'admin',
        'os_tenant_name': 'admin',
        'os_password': '12345'},
    'log': {
        'handler': 'console, rotating',
        'path': '/var/log/cds/cds-agent.log',
        'max_bytes': '1*1024*1024',
        'back_count': 5,
        'level': '1'},
    'float_ip': {
        'api': 'openstack_api'},
    'fetch': {
        'src': 'mongodb'},
    'push': {
        'dest': 'mysqldb'},
    'nic': {
        'interval': 180},
    'disk': {
        'interval': 240},
    'load': {
        'interval': 60}}


class Section(object):

    def __init__(self, **kwargs):
        for k, v in kwargs.items():
            setattr(self, k, v)

    def update(self, k, v):
        setattr(self, k, v)


class CoreSection(Section):

    name = 'core'

    def __init__(self):
        kw = _DEFAULT_CONFIG.get(self.name)
        super(CoreSection, self).__init__(**kw)


class DatabaseSection(Section):

    name = 'database'

    def __init__(self):
        kw = _DEFAULT_CONFIG.get(self.name)
        super(DatabaseSection, self).__init__(**kw)


class FetchSection(Section):

    name = 'fetch'

    def __init__(self):
        kw = _DEFAULT_CONFIG.get(self.name)
        super(FetchSection, self).__init__(**kw)


class PushSection(Section):

    name = 'push'

    def __init__(self):
        kw = _DEFAULT_CONFIG.get(self.name)
        super(PushSection, self).__init__(**kw)


class MysqlSection(Section):

    name = 'mysql'

    def __init__(self):
        kw = _DEFAULT_CONFIG.get(self.name)
        super(MysqlSection, self).__init__(**kw)


class KeyStoneSection(Section):

    name = 'keystone'

    def __init__(self):
        kw = _DEFAULT_CONFIG.get(self.name)
        super(KeyStoneSection, self).__init__(**kw)


class FloatIpSection(Section):

    name = 'float_ip'

    def __init__(self):
        kw = _DEFAULT_CONFIG.get(self.name)
        super(FloatIpSection, self).__init__(**kw)


class LogSection(Section):

    name = 'log'

    def __init__(self):
        kw = _DEFAULT_CONFIG.get(self.name)
        super(LogSection, self).__init__(**kw)


class NicSection(Section):

    name = 'nic'

    def __init__(self):
        kw = _DEFAULT_CONFIG.get(self.name)
        super(NicSection, self).__init__(**kw)


class DiskSection(Section):

    name = 'disk'

    def __init__(self):
        kw = _DEFAULT_CONFIG.get(self.name)
        super(DiskSection, self).__init__(**kw)


class LoadSection(Section):

    name = 'load'

    def __init__(self):
        kw = _DEFAULT_CONFIG.get(self.name)
        super(LoadSection, self).__init__(**kw)


class Factory():
    def get_section(self, name):
        sections = {
            'core': lambda: CoreSection(),
            'database': lambda: DatabaseSection(),
            'mysql': lambda: MysqlSection(),
            'keystone': lambda: KeyStoneSection(),
            'float_ip': lambda: FloatIpSection(),
            'fetch': lambda: FetchSection(),
            'push': lambda: PushSection(),
            'log': lambda: LogSection(),
            'nic': lambda: NicSection(),
            'disk': lambda: DiskSection(),
            'load': lambda: LoadSection()}
        return sections[name]()


class Config():

    f = Factory()

    def __init__(self):
        keys = _DEFAULT_CONFIG.keys()
        for k in keys:
            setattr(self, k, Config.f.get_section(k))

    def _is_exists(self, config_file):
        if not os.path.exists(config_file):
            return False
        else:
            return True

    def __call__(self, config_file):
        try:
            if not self._is_exists(config_file):
                raise exc.NotFoundConfigureFile('Not Found \
                        config file', '0000-001-01')
            conf = ConfigParser.ConfigParser()
            conf.read(config_file)
            for k in conf.sections():
                p = getattr(self, k, None)
                if not p:
                    setattr(self, k, Config.f.get_section(k))
                options = conf.options(k)
                for option in options:
                    p.update(option, conf.get(k, option))
        except Exception, e:
            raise exc.ConfigureException(str(e))


def reload_config():
    Config(_configure_file)

CONF = Config()
# CONF(_configure_file)
