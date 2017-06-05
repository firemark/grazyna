from grazyna.irc.message_controller import MessageController
from unittest.mock import Mock


def execute_message(protocol, data):
    ctrl = MessageController(protocol, data)
    ctrl.log = Mock()
    ctrl.execute_message()
    return ctrl
