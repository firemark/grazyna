from grazyna.tests.commands.base import execute_message


def test_part_without_reason(protocol):
    ctrl = execute_message(protocol, [':socek!a@b', 'PART', '#czarnobyl'])
    assert protocol.messages == []
    ctrl.log.assert_called_once_with('#czarnobyl', 'socek::PART')


def test_part_with_reason(protocol):
    data = [':socek!a@b', 'PART', '#czarnobyl', 'dunno lol']
    ctrl = execute_message(protocol, data)
    assert protocol.messages == []
    ctrl.log.assert_called_once_with('#czarnobyl', 'socek::PART[dunno lol]')
