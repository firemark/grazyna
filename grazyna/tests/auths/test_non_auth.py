from grazyna.auths import NonAuth


def test_non_auth(protocol):
    auth = NonAuth()
    auth.auth(protocol)
    assert protocol.messages == []
