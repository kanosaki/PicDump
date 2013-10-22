import collections

from .base import Source


# cyclic([A, B, C, D], [1, 2], [a]) -> [A, 1, a, B, 2, C, D]
class CyclicJunction(Source):
    def __init__(self, *parents: tuple):
        self.parents = parents
        self._init()

    def _init(self):
        self.live_sources = collections.deque(self.parents)

    def __next__(self):
        try:
            next_source = self.live_sources.popleft()
        except IndexError:
            raise StopIteration()
        try:
            next_elem = next(next_source)
            self.live_sources.append(next_source)
            return next_elem
        except StopIteration:
            # remove next_source from live_sources since it has no elements
            return next(self)

    def __iter__(self):
        return type(self)(*self.parents)

    def reset(self):
        for parent in self.parents:
            parent.reset()
        self._init()
