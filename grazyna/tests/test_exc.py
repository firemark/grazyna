from grazyna.irc.exc import NoSuchNickError


def test_str_method():
    assert str(NoSuchNickError('socek')) == 'NoSuchNickError(socek)'
