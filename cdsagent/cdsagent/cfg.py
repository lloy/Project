
import ConfigParser
import os


from cdsagent import exc


__author__ = 'Hardy.zheng'

_DEFAULT_CONFIG = {
    'core': {
        'interval': 600},
    'database': {
        'connection': None},
    'log': {
        'path': '/var/log/cds/cds-agent.log',
        'level': 1},
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
                raise exc.NotFoundConfigureFile('Not Found config file', '0000-001-01')
            conf = ConfigParser.ConfigParser()
            conf.read(config_file)
            for k in conf.sections():
                p = getattr(self, k, None)
                options = conf.options(k)
                for option in options:
                    p.update(option, conf.get(k, option))
        except Exception, e:
            print e


def reload_config():
    CONF(_config_file)


CONF = Config()
_config_file = './cds.cfg'

CONF(_config_file)
