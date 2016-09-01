#!/usr/bin/python3

import asyncio
#import pyejdb
from grazyna.db import get_engine, get_session
import re
import datetime

from .message_controller import MessageController
from .sender import IrcSender

re_message = re.compile(
    r'(?:(:[^ ]+) )?'
    r'([^:\r]+)'
    r'(?: :([^\r]+))?'
    r'\r\n'
)


class IrcClient(asyncio.Protocol, IrcSender):
    ready = False
    config = None
    importer = None
    db = None
    connection_lost_future = None
    ping_counter = 0

    def __init__(self, config, connection_lost_future):
        IrcSender.__init__(self)
        asyncio.Protocol.__init__(self)
        self.config = config
        self.importer = self.config.getmodule('main', 'importer')(self)
        self.importer.load_all()
        if 'db_uri' in config['main']:
            self.db = get_engine(config['main']['db_uri'])
        self.connection_lost_future = connection_lost_future

    def connection_made(self, transport):
        config = self.config['main']
        self.transport = transport
        self.send('PASS', config['password'])
        self.send('NICK', config['nick'])
        self.send_msg('USER', config['ircname'], 'wr', '*', config['realname'])

    def data_received(self, raw_messages):
        codecs = self.config.getlist('main', 'codecs')
        for message in self._parse_raw_messages(raw_messages, codecs):
            MessageController(self, message).execute_message()

    def connection_lost(self, exc):
        self.connection_lost_future.set_exception(exc)
        self.importer.cancel_tasks()

    def get_session(self):
        session = get_session(self.db)
        return session.scope()

    @staticmethod
    def _parse_raw_messages(raw_messages, codecs=('utf-8',)):
        for codec in codecs:
            try:
                encoded_data = raw_messages.decode(codec)
            except UnicodeDecodeError:
                continue
            else:
                break
        else:
            return

        for match in re_message.finditer(encoded_data):
            prefix, messages, long_message = match.groups()
            data = [prefix] if prefix else []
            data += messages.split()
            if long_message:
                data.append(long_message)
            yield data


def connect(config):
    loop = asyncio.get_event_loop()
    try:
        while True:
            main_config = config['main']
            future = asyncio.Future()
            factory = lambda: IrcClient(config, future)
            coro = loop.create_connection(
                factory, main_config['host'], main_config['port']
            )
            loop.run_until_complete(coro)
            loop.run_until_complete(future)
    finally:
        loop.close()
