from asyncio import Future
from grazyna.irc.client import IrcClient as DefaultIrcClient
from grazyna.irc.models import WhoisData
from grazyna.test_mocks.sender import IrcSender, Message
from grazyna.config import create_empty_config
from unittest.mock import Mock, patch, call

import pytest
import asyncio


class IrcClient(DefaultIrcClient, IrcSender):
    pass


def make_client(**dict_cfg):
    config = create_empty_config()
    config.read_dict({'main': {
        'importer': 'grazyna.test_mocks.importer.Importer',
    }})
    config.read_dict(dict_cfg)
    return IrcClient(config, Future())


def test_init():
    client = make_client()
    assert client.importer.is_loaded is True
    assert client.importer.protocol is client


def test_connection_made():
    client = make_client(main=dict(
        nick='socek',
        password='klocek',
        ircname='superSocek',
        realname='realSocek',
    ))
    transport = Mock()
    client.connection_made(transport)
    assert client.transport is transport
    assert client.messages == [
        Message('PASS', 'klocek'),
        Message('NICK', 'socek'),
        Message('USER', 'superSocek', 'wr', '*', ':realSocek'),
    ]


@patch('grazyna.irc.client.MessageController')
def test_data_received(message_controller):
    client = make_client(main=dict(codecs=['utf-8']))
    msg1 = b':Angel PRIVMSG Wiz :Hello tl;dr\r\n'
    msg2 = b'PONG csd.bu.edu tolsun.oulu.fi\r\n'
    client.data_received(msg1 + msg2)
    assert message_controller.call_args_list == [
        call(client, [':Angel', 'PRIVMSG', 'Wiz', 'Hello tl;dr']),
        call(client, ['PONG', 'csd.bu.edu', 'tolsun.oulu.fi']),
    ]


@patch('grazyna.irc.client.MessageController')
def test_wrong_data_received(message_controller):
    client = make_client(main=dict(codecs=['utf-8']))
    client.data_received(b'\xFF\r\n')
    assert message_controller.call_args_list == []


def test_connection_lost():
    client = make_client()
    exc = Exception('socek')
    client.connection_lost(exc)
    assert client.connection_lost_future.exception() == exc
    assert client.importer.is_canceled is True


def test_db_scope():
    client = make_client(main=dict(db_uri='sqlite://'))
    session = client.get_session()
    assert session is not None


@pytest.mark.asyncio
def test_whois():
    client = make_client()

    @asyncio.coroutine
    def set_whois():
        yield from asyncio.sleep(0.5)
        future = client.whois_heap['socek']
        future.data.nick = 'socek'
        future.set_result(future.data)

    result, _ = yield from asyncio.gather(
        client.whois('socek'),
        set_whois()
    )

    assert isinstance(result, WhoisData)
    assert result.nick == 'socek'
