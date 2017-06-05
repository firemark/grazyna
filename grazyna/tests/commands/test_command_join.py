from grazyna.tests.commands.base import execute_message


def test_join(protocol):
    ctrl = execute_message(protocol, [':socek!a@b', 'JOIN', '#czarnobyl'])
    assert protocol.messages == []
    ctrl.log.assert_called_once_with('#czarnobyl', 'socek(a@b)::JOIN')
