from grazyna.request import RequestBot
from grazyna.test_mocks.sender import SayMessage, Message
from grazyna.irc.models import User


def make_bot(protocol, **kwargs):
    return RequestBot(protocol, user=User('socek!a@b'), chan='#czarnobyl', **kwargs)


def test_init(protocol):
    bot = RequestBot(protocol)
    assert bot.protocol is protocol


def test_nick_chan_on_privmsg(protocol):
    bot = make_bot(protocol, private=True)
    assert bot.nick_chan == 'socek'


def test_nick_chan_on_channel(protocol):
    bot = make_bot(protocol)
    assert bot.nick_chan == '#czarnobyl'


def test_say(protocol):
    bot = make_bot(protocol)
    bot.say('foobar')
    assert protocol.messages == [SayMessage('#czarnobyl', 'foobar')]


def test_notice(protocol):
    bot = make_bot(protocol)
    bot.notice('foobar')
    assert protocol.messages == [Message('NOTICE', 'socek', ':foobar')]


def test_reply(protocol):
    bot = make_bot(protocol)
    bot.reply('foobar')
    assert protocol.messages == [SayMessage('#czarnobyl', 'socek: foobar')]


def test_kick(protocol):
    bot = make_bot(protocol)
    bot.kick(who='firemark', why='dunno lol')
    assert protocol.messages == [Message('KICK', '#czarnobyl', 'firemark', ':dunno lol')]


def test_kick_on_private(protocol):
    bot = make_bot(protocol, private=True)
    bot.kick()  # is not possible to kick on private message
    assert protocol.messages == []
    

def test_private_say(protocol):
    bot = make_bot(protocol)
    bot.private_say('foobar')
    assert protocol.messages == [SayMessage('socek', 'foobar')]


def test_command(protocol):
    bot = make_bot(protocol)
    bot.command('WTF')
    assert protocol.messages == [Message('WTF')]


def test_command_msg(protocol):
    bot = make_bot(protocol)
    bot.command_msg('WTF', 'dunno lol')
    assert protocol.messages == [Message('WTF', ':dunno lol')]


def test_mode(protocol):
    bot = make_bot(protocol)
    bot.mode('#czarnobyl', '+oo', 'lol')
    assert protocol.messages == [Message('MODE', 'lol', '#czarnobyl', '+oo')]
