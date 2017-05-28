from grazyna.irc.sender import IrcSender as DefaultIrcSender
import pytest


@pytest.fixture()
def protocol():
    return IrcSender()


class IrcSender(DefaultIrcSender):

    def __init__(self):
        super().__init__()
        self.messages = []

    def send(self, *args):
        self.messages.append(Message(*args))

    def send_msg(self, *args):
        *args, tail = args
        self.messages.append(Message(*args, tail))


class Message(list):

    def __init__(self, *args):
        arg, *args = args
        super().__init__([arg.upper(), *args])


class SayMessage(Message):

    def __init__(self, to, msg):
        super().__init__('PRIVMSG', to, msg)

