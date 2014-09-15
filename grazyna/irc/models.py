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

    def __init__(*args, **kwargs):
        super().__init__(*args, **kwargs)
        self.data = WhoisData()


class WhoisData(object):

    idle = 0
    account = None
    ircname = None
    host = None
    channels = None

    def __init__(self):
        self.channels = []
