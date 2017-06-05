from grazyna.tests.commands.base import execute_message
from grazyna.irc.models import User

import pytest


@pytest.mark.asyncio
def test_notice(protocol_with_importer, event_loop):
    yield from []  # noqa - turn on global event_loop
    data = [':socek!a@b', 'NOTICE', '#czarnobyl', 'message']
    ctrl = execute_message(protocol_with_importer, data)

    def check(ctrl):  # wait for another coroutines
        importer = protocol_with_importer.importer
        assert protocol_with_importer.messages == []
        assert importer.execute.assert_called_once_with(
            '#czarnobyl', User('socek!a@b'), 'message'
        )

        ctrl.log.assert_called_once_with('#czarnobyl', '<socek> message')
    event_loop.call_soon(check, ctrl)
