from unittest.mock import Mock
from asyncio import coroutine


class AsyncMock(Mock):

    @coroutine
    def __call__(self, *args, **kwargs):
        return super().__call__(*args, **kwargs)


class Importer(object):
    protocol = None
    is_loaded = False
    is_canceled = True
    whois_heap = {}

    def __init__(self, protocol):
        self.protocol = protocol
        self.execute = AsyncMock()
        self.load = Mock()
        self.reload = Mock()
        self.remove = Mock()

    def load_all(self):
        self.is_loaded = True

    def cancel_tasks(self):
        self.is_canceled = True
