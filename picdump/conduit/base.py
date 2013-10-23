
class Source:
    def __init__(self, parent=None):
        self.parent = parent

    def reset(self):
        if self.parent is not None:
            self.parent.reset()

    def __iter__(self):
        self.reset()
        return self
