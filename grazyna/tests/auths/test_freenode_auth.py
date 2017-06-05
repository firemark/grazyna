from grazyna.auths import FreenodeAuth
from grazyna.test_mocks.sender import SayMessage


def test_freenode_auth(protocol):
    auth = FreenodeAuth('klocek')
    auth.auth(protocol)
    assert protocol.messages == [
        SayMessage('nickserv', 'identify klocek'),
    ]
