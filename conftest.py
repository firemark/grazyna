from grazyna.test_mocks.sender import IrcSender
from grazyna.test_mocks.importer import Importer
from grazyna.request import RequestBot
from grazyna.irc.models import User

import pytest


@pytest.fixture()
def protocol():
    return IrcSender()


@pytest.fixture()
def protocol_with_importer():
    client = IrcSender()
    client.importer = Importer(client)
    return client


@pytest.fixture
def public_bot(protocol):
    bot = RequestBot(protocol)
    bot.user = User('socek!a@b')
    bot.chan = '#czarnobyl'
    bot.private = False
    return bot


@pytest.fixture
def private_bot(protocol):
    bot = RequestBot(protocol)
    bot.user = User('socek!a@b')
    bot.private = True
    return bot


@pytest.fixture
def bot_with_importer(protocol_with_importer):
    bot = RequestBot(protocol_with_importer)
    bot.user = User('socek!a@b')
    bot.chan = '#czarnobyl'
    return bot
