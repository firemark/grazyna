from grazyna.tests.commands.base import execute_message
from grazyna.irc.exc import NoSuchNickError
from grazyna.irc.models import WhoisFuture


def test_command_no_such_nick(protocol):
    data = [
        ':server', '401', 'bot',
        'socek', ':No such nick/channel',
    ]
    future = protocol.whois_heap['socek'] = WhoisFuture()
    execute_message(protocol, data)
    assert protocol.whois_heap == {}
    assert future.exception() == NoSuchNickError('socek')
