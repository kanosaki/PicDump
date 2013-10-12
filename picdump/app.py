

class App:
    """Application root context"""
    def __init__(self, config):
        self.config = config

    def start(self):
        for folder in self.config.folders:
            folder.start_dump()


class Dumper:
    def __init__(self, config):
        self.config = config