from .filter import PassFilter


class Source:
    def __init__(self, filter=None):
        self.filter = filter or PassFilter.default

    def reset(self):
        self.filter.reset()

    def __iter__(self):
        return self
