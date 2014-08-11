#from cdsagent.utils import fixpath
import ConfigParser
import os


_DEFAULT_CONFIG = {

        'core':{
            'interval' : 600
            },
        'database':{
            'connection':None
            },
        'log':{
            'log_path':'/var/log/cds/cds-agent.log',
            'log_level':1,
            },
        'nic':{
            'interval':180,
            },
        'disk':{
            'interval':240
            },
        'load':{

            'interval':60
            }
        }


class Section(object):

    def __init__(self, **kwargs):
        for k ,v in kwargs.items():
            setattr(self, k, v)

    def update(self, k, v):
        setattr(self, k ,v)

class CoreSection(Section):

    _name = 'core'

    def __init__(self):
        kw = _DEFAULT_CONFIG.get(self._name)
        super(CoreSection, self).__init__(**kw)

class DatabaseSection(Section):

    _name = 'database'

    def __init__(self):
        kw = _DEFAULT_CONFIG.get(self._name)
        super(DatabaseSection, self).__init__(**kw)

class LogSection(Section):

    _name = 'log'

    def __init__(self):
        kw = _DEFAULT_CONFIG.get(self._name)
        super(LogSection, self).__init__(**kw)

class NicSection(Section):

    _name = 'nic'

    def __init__(self):
        kw = _DEFAULT_CONFIG.get(self._name)
        super(NicSection, self).__init__(**kw)

class DiskSection(Section):

    _name = 'disk'

    def __init__(self):
        kw = _DEFAULT_CONFIG.get(self._name)
        super(DiskSection, self).__init__(**kw)

class LoadSection(Section):

    _name = 'load'

    def __init__(self):
        kw = _DEFAULT_CONFIG.get(self._name)
        super(LoadSection, self).__init__(**kw)

class Factory():
    def get_section(self, name):
        sections = {
                'core':lambda:CoreSection(),
                'database':lambda:DatabaseSection(),
                'log':lambda:LogSection(),
                'nic':lambda:NicSection(),
                'disk':lambda:DiskSection(),
                'load':lambda:LoadSection(),
                }
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

# tasks = {
    # 'nic': lambda: task_nic(),
    # 'mem': lambda: task_disk(),
    # 'load': lambda: task_load()}


# def task_nic():
    # print "i' am nic task"


# def task_disk():
    # print "i' am disk task"


# def task_load():
    # print "i' am load task"


# if __name__ == '__main__':

    # for name in tasks:
        # s =  getattr(CONF, name, 60)
        # if isinstance(s, Section):
            # print  s.interval

        # else:
            # print s
        # tasks[name]()

    #import time
    #counter = 0
    #while True:
        ##conf = Config()
        ##conf(config_file)
        #print CONF.core.interval
        #if counter == 4:
            #reload_config()
        #if counter == 8:
            #reload_config()
        #counter += 1
        #time.sleep(4)

        ##print conf.log.handler
        ##conf = ConfigParser.ConfigParser()
        ##conf.read(config_file)
        ##c= conf.get('log', 'handler')

