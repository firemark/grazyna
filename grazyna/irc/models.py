import asyncio


class User(object):
    """User class - has nick, realname, and host"""
    nick = ""
    host = ""
    realname = ""

    def __init__(self, prefix):
        try:
            self.nick, name_host = prefix.split('!')
            self.realname, self.host = name_host.split('@')
        except:
            pass

    @property
    def prefix(self):
        return "%s@%s" % (self.realname, self.host)


class WhoisFuture(asyncio.Future):

    data = None

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.data = WhoisData()


class WhoisData(object):

    __slots__ = ('idle', 'account', 'ircname', 'host',
                 'channels', 'realname', 'server', 'nick')

    def __init__(self):
        self.channels = []
        self.idle = 0
        self.nick = None
        self.account = None
        self.ircname = None
        self.host = None
        self.realname = None
