from grazyna.auths import QuakenetAuth
from grazyna.test_mocks.sender import SayMessage


def test_quakenet_auth(protocol):
    auth = QuakenetAuth('socek', 'klocek')
    auth.auth(protocol)
    assert protocol.messages == [
        SayMessage('Q@CServe.quakenet.org', 'AUTH socek klocek'),
    ]
