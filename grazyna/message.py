from .irc import User
from . import irc, log, config
from . import is_admin_con, waiting_events

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
        method = getattr(self, 'command_%s' % self.command.lower())

        if method is not None:
            method()

    def command_join(self):
        channel = self.data[2]
        log.write(channel, '%s(%s)::JOIN' % (self.user.nick, self.user.prefix))

    def command_part(self):
        channel = self.data[2]
        if len(self.data) == 4:
            reason = self.data[3]
            log.write(channel, "%s::PART[%s]" % (self.user.nick, reason))
        else:
            log.write(data[2], "%s::PART" % self.user.nick)

    def command_kick(self):
        channel, nick = data[2:4]
        log.write(channel, "%s KICK %s" % (self.user.nick, nick))

                  

        if data[3] == config.nick:
            irc.join(data[2])        

    def command_error(self):
        pass

    def command_privmsg(self):
        channel, text = data[2:]
        log.write(chan, "<%s> %s" % (user.nick, text))
        waiting_events.put_nowait((
            "msg", user, {"chan": chaNELn, "txt": text}
        ))

    def command_notice(self):
        self.command_privmsg()