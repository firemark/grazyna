from grazyna.auths import NonAuth
from grazyna.test_mocks.sender import protocol


def test_non_auth(protocol):
    auth = NonAuth()
    auth.auth(protocol)
    assert protocol.messages == [] 

