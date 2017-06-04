from grazyna.irc.sender import IrcSender as DefaultIrcSender
from grazyna.config import create_empty_config
from grazyna.test_mocks.importer import Importer
import pytest


@pytest.fixture()
def protocol():
    return IrcSender()


@pytest.fixture()
def protocol_with_importer():
    client = IrcSender()
    client.importer = Importer(client)
    return client


class IrcSender(DefaultIrcSender):
    ready = False
    messages = None
    config = None

    def __init__(self):
        super().__init__()
        self.messages = []
        self.config = config = create_empty_config()
        config.read_dict(dict(
            main=dict(
                importer='grazyna.test_mocks.importer.Importer',
            ),
            auth=dict(
                module='grazyna.auths.NonAuth',
            )
        ))

    def send(self, *args):
        self.messages.append(Message(*args))


class Message(list):

    def __init__(self, *args):
        arg, *args = args
        super().__init__([arg.upper()] +  args)


class SayMessage(Message):

    def __init__(self, to, msg):
        super().__init__('PRIVMSG', to, ':' + msg)
