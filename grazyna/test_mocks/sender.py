from grazyna.db import get_session
from grazyna.irc.sender import IrcSender as DefaultIrcSender
from grazyna.config import create_empty_config
from grazyna.test_mocks.importer import Importer

from unittest.mock import Mock
from asyncio import BaseTransport



class IrcSender(DefaultIrcSender):
    ready = False
    messages = None
    config = None
    db = None
    transport = None
    ping_counter = 0

    def __init__(self):
        super().__init__()
        self.messages = []
        self.config = config = create_empty_config()
        self.transport = Mock(spec=BaseTransport)
        self.importer = Importer(self)
        config.read_dict(dict(
            main={
                'nick': 'bot',
                'importer': 'grazyna.test_mocks.importer.Importer',
                'command-prefix': '.',
                'time_to_block': '30',
                'executed_commands_per_time': '20',
                'db_uri': 'sqlite://',
            },
            auth=dict(
                module='grazyna.auths.NonAuth',
            )
        ))

    def send(self, *args):
        self.messages.append(Message(*args))

    def get_session(self):
        return get_session(self.db).scope()


class Message(list):

    def __init__(self, *args):
        arg, *args = args
        super().__init__([arg.upper()] + args)


class SayMessage(Message):

    def __init__(self, to, msg):
        super().__init__('PRIVMSG', to, ':' + msg)
