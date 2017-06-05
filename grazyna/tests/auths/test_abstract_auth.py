from grazyna.auths import AbstractAuth
import pytest


@pytest.fixture
def auth():
    return AbstractAuth()


def test_abstract_auth_add_permission(auth):
    with pytest.raises(NotImplementedError):
        auth.add_permission('test', '#test', 0)


def test_abstract_auth_check_permission(auth):
    with pytest.raises(NotImplementedError):
        auth.check_permission('test', '#test', 0)


def test_abstract_auth__auth_method(auth):
    with pytest.raises(NotImplementedError):
        auth.auth()
