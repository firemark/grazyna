from grazyna.test_mocks.sender import IrcSender
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
