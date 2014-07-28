from .irc import User

class MessageController(object):

    command = ''
    prefix = ''
    user = None
    data = None

    def __init__(self, command, data):
        self.prefix, self.command = data[0:2]
        self.data = data
        self.user = User(self.prefix)

    def execute_message(self):
        method = getattr(self, 'command_%s' % self.command)

        if method is not None:
            method()


