
class Folder:
    def __init__(self, path=None, source=None, updater=None):
        if path is None:
            raise "path required"
        if source is None:
            raise "source for {} is required".format(path)
        if updater is None:
            raise "update for {} is required".format(path)
        self.path = path
        self.source = source
        self.updater = updater
