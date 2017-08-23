from grazyna.plugins.db import add_cmd, delete_cmd
from grazyna.test_mocks.sender import SayMessage
from grazyna.models import Message

import pytest


@pytest.mark.asyncio
def test_db_add(public_bot_with_db):
    yield from add_cmd(public_bot_with_db, 'firemark', 'firesmart')
    yield from add_cmd(public_bot_with_db, 'firemark', 'firesmark')

    with public_bot_with_db.protocol.get_session() as session:
        data = session.query(Message.message).filter_by(
            key='firemark',
            channel='#czarnobyl',
        ).all()

    assert set(o[0] for o in data) == {'firesmart', 'firesmark'}
    assert public_bot_with_db.protocol.messages == [
        SayMessage('#czarnobyl', 'socek: Done!'),
        SayMessage('#czarnobyl', 'socek: Done!'),
    ]


@pytest.mark.asyncio
def test_db_delete(public_bot_with_db):
    msg = Message()
    msg.channel = '#czarnobyl'
    msg.key = 'gjm'
    msg.message = '??'
    with public_bot_with_db.protocol.get_session() as session:
        session.add(msg)
        session.add(msg)

    yield from delete_cmd(public_bot_with_db, 'gjm')

    with public_bot_with_db.protocol.get_session() as session:
        obj = session.query(Message).filter_by(
            key='gjm', channel='#czarnobyl'
        ).first()
    assert obj is None
    assert public_bot_with_db.protocol.messages == [
        SayMessage('#czarnobyl', 'socek: Done!'),
    ]


@pytest.mark.asyncio
def test_db_delete_doesnt_exist(public_bot_with_db):
    yield from delete_cmd(public_bot_with_db, 'gjm')
    assert public_bot_with_db.protocol.messages == [
        SayMessage('#czarnobyl', 'socek: Key doesn\'t exist'),
    ]

