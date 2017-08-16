import asyncio


class User(object):
    """User class - has nick, realname, and host"""
    nick = ""
    host = ""
    realname = ""

    def __init__(self, prefix):
        try:
            self.nick, _, name_host = prefix.partition('!')
            self.realname, _, self.host = name_host.partition('@')
        except:
            pass

    @property
    def prefix(self):
        return "%s@%s" % (self.realname, self.host)

    def __repr__(self):
        return "User('%s!%s')" % (self.nick, self.prefix)

    def __eq__(self, other):
        if not isinstance(other, type(self)):
            return False

        return (
            self.nick == other.nick
            and self.realname == other.realname
            and self.host == other.host
        )


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
