from grazyna.db import get_engine, create_database
from grazyna.test_mocks.sender import IrcSender
from grazyna.test_mocks.importer import Importer
from grazyna.request import RequestBot
from grazyna.irc.models import User

import pytest


@pytest.fixture()
def protocol():
    return IrcSender()


@pytest.fixture()
def protocol_with_db():
    client = IrcSender()
    db_uri = client.config.get('main', 'db_uri')
    client.db = get_engine(db_uri)
    create_database(client.db)
    return client


@pytest.fixture()
def protocol_with_importer():
    client = IrcSender()
    client.importer = Importer(client)
    return client


@pytest.fixture
def public_bot(protocol):
    return RequestBot(
        protocol=protocol,
        user=User('socek!a@b'),
        chan='#czarnobyl',
        private=False,
        config={},
        temp={},
    )


@pytest.fixture
def private_bot(protocol):
    return RequestBot(
        protocol=protocol,
        user=User('socek!a@b'),
        private=True,
        config={},
        temp={},
    )



@pytest.fixture
def bot_with_importer(protocol_with_importer):
    return RequestBot(
        protocol=protocol_with_importer,
        user=User('socek!a@b'),
        chan='#czarnobyl',
    )
