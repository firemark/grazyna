class Importer(object):
    protocol = None
    is_loaded = False
    is_canceled = True

    def __init__(self, protocol):
        self.protocol = protocol

    def load_all(self):
        self.is_loaded = True

    def cancel_tasks(self):
        self.is_canceled = True

