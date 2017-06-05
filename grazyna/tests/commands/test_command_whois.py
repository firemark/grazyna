from grazyna.tests.commands.base import execute_message
from grazyna.irc.models import WhoisFuture


def test_whois_user(protocol):
    data = [
        ':server', '311', 'bot',
        'socek', 'realsocek', 'onet.pl', '*', 'the socketor',
    ]
    future = protocol.whois_heap['socek'] = WhoisFuture()
    execute_message(protocol, data)
    assert future.data.nick == 'socek'
    assert future.data.ircname == 'the socketor'
    assert future.data.host == 'onet.pl'
    assert future.data.realname == 'realsocek'


def test_whois_user_without_trigger(protocol):
    data = [
        ':server', '311', 'bot',
        'socek', 'realsocek', 'onet.pl', '*', 'the socketor',
    ]
    execute_message(protocol, data)
    assert 'socek' not in protocol.whois_heap


def test_whois_server(protocol):
    data = [':server', '312', 'bot', 'socek', 'banana server']
    future = protocol.whois_heap['socek'] = WhoisFuture()
    execute_message(protocol, data)
    assert future.data.server == 'banana server'


def test_whois_idle(protocol):
    data = [':server', '317', 'bot', 'socek', '30', 'seconds idle']
    future = protocol.whois_heap['socek'] = WhoisFuture()
    execute_message(protocol, data)
    assert future.data.idle == 30


def test_whois_channels(protocol):
    data = [':server', '319', 'bot', 'socek', '#foo #bar']
    future = protocol.whois_heap['socek'] = WhoisFuture()
    execute_message(protocol, data)
    assert future.data.channels == ['#foo', '#bar']


def test_whois_account(protocol):
    data = [':server', '330', 'bot', 'socek', 'socketor']
    future = protocol.whois_heap['socek'] = WhoisFuture()
    execute_message(protocol, data)
    assert future.data.account == 'socketor'


def test_whois_end(protocol):
    data = [':server', '318', 'bot', 'socek', 'End of /WHOIS list']
    future = protocol.whois_heap['socek'] = WhoisFuture()
    execute_message(protocol, data)
    assert future.result() is future.data
