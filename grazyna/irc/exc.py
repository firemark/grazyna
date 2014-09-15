class NoSuchNickError(Exception):

    nick = None
    
    def __init__(self, nick):
        self.nick = nick

    def __repr__(self):
        return 'NoSuchNickError(%s)' % self.nick

    def __str__(self):
        return repr(self)