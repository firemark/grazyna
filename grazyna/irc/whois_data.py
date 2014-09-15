import asyncio


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
