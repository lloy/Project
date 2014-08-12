
__author__ = 'Hardy.zheng'


class AgentException(Exception):

    errno = '0000-000-00'

    def __init__(self, message, errno):
        self.msg = message
        self.code = errno
        super(AgentException, self).__init__(self.msg, self.code)


class RunNovaClientError(AgentException):

    def __init__(self, message):
        errno = '0000-005-01'
        super(RunNovaClientError, self).__init__(message, errno)


class ConfigureException(AgentException):

    """
    errno = 0000-001-00
    """

    def __init__(self, message):
        errno = '0000-001-00'
        super(ConfigureException, self).__init__(message, errno)


class NotSetPoller(ConfigureException):
    """
    errno = 0000-001-02
    """
    pass


class NotRunMethod(AgentException):
    """
    errno = 0000-003-01
    """
    pass


class NotFoundConfigureFile(ConfigureException):
    """
    errno = 0000-001-01
    """
    pass


class MultipleResultsFound(AgentException):
    pass


class NoResultFound(AgentException):
    pass


class BadVersion(AgentException):
    """ code: 0000-000-02 """
    pass


class BadAggregate(AgentException):
    pass
