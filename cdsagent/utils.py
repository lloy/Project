import os
from six.moves.urllib import parse

__author__ = 'Hardy.zheng'


def urlsplit(url, scheme='', allow_fragments=True):
    scheme, netloc, path, query, fragments = parse.urlsplit(url, scheme, allow_fragments)
    return scheme

def fixpath(p):
    return os.path.abspath(os.path.expanduser(p))
