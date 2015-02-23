#from . import irc


class AbstractAuth(object):

    def add_permission(self, username, channel, level):
        raise NotImplementedError('add_permission')

    def check_permission(self, username, channel, level):
        raise NotImplementedError('check_permission')

    def auth(self):
        raise NotImplementedError('auth')


class NonAuth(AbstractAuth):

    def auth(self, protocol):
        pass

class QuakenetAuth(AbstractAuth):

    user = None
    passwd = None

    def __init__(self, user, passwd):
        self.user = user
        self.passwd = passwd

    def auth(self, protocol):
        protocol.say('Q@CServe.quakenet.org AUTH {0.user} {0.passwd}'.format(self))


class FreenodeAuth(AbstractAuth):

    passwd = None

    def __init__(self, passwd):
        self.passwd = passwd

    def auth(self, protocol):
        protocol.say('nickserv', 'identify %s' % self.passwd)