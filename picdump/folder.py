
class Folder:
    def __init__(self, path=None, source=None, updater=None):
        if path is None:
            raise Exception("path required")
        if source is None:
            raise Exception("source for {} is required".format(path))
        if updater is None:
            raise Exception("update for {} is required".format(path))
        self.path = path
        self.source = source
        self.updater = updater
