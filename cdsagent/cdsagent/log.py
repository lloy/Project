import logging
from logging import handlers as loghandlers
from cdsagent import cfg

DEAFAULT_SIGN = ','
LOG_LEVEL = {
    '0': logging.INFO,
    '1': logging.DEBUG,
    '2': logging.WARNING,
    '3': logging.ERROR,
    '4': logging.CRITICAL}


class Logger(object):

    def __init__(self, level, path, handlers, max_bytes, back_count):
        self.level = LOG_LEVEL.get(level) if level else logging.INFO
        self.formatter = '%(asctime)s %(filename)s[line:%(lineno)d] \
                %(levelname)s %(message)s'
        self.datefmt = '%a, %d %b %Y %H:%M:%S'
        self.filename = path
        self.filemode = 'a'
        self.max_bytes = max_bytes
        self.back_count = back_count
        self._handlers = handlers

    def set_handler(self):
        for h in self._handlers:
            if h == 'console':
                console = logging.StreamHandler()
                console.setLevel(self.level)
                formatter = logging.Formatter(self.formatter)
                console.setFormatter(formatter)
                logging.getLogger('').addHandler(console)
            if h == 'rotating':
                rotating = loghandlers.RotatingFileHandler(self.filename, maxBytes=self.max_bytes, backupCount=self.back_count)
                rotating.setLevel(self.level)
                formatter = logging.Formatter(self.formatter)
                rotating.setFormatter(formatter)
                logging.getLogger('').addHandler(rotating)

    def setup(self, name):
        logging.basicConfig(level=self.level,
                            format=self.formatter,
                            datefmt=self.datefmt,
                            filename=self.filename,
                            filemode=self.filemode)
        self.set_handler()
        return logging.getLogger(name)

level = cfg.CONF.log.level
print level
path = cfg.CONF.log.path
log_handlers = [h.strip() for h in cfg.CONF.log.handler.split(DEAFAULT_SIGN)]
max_bytes = cfg.CONF.log.max_bytes
count = cfg.CONF.log.back_count

logger = Logger(level, path, log_handlers, max_bytes, count)
LOG = logger.setup('cds-agent')
