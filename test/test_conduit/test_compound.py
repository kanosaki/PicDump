from nose.tools import *

utils = __import__('utils')  # Suppress PyCharm warning
from picdump import conduit


class DummySource:
    def __init__(self, src):
        self.src = src
        self.it = None
        self.reset()

    def __next__(self):
        return next(self.it)

    def reset(self):
        self.it = iter(self.src)


def src(iterable):
    return DummySource(iterable)


class TestCompound:
    def test_unique_cycle(self):
        src_a = src([1, 2, 3, 4])
        src_b = src([])
        src_c = src(['a', 1, 5, 'b'])
        source = conduit.unique(conduit.cyclic(src_a, src_b, src_c))
        assert_list_equal([1, 'a', 2, 3, 5, 4, 'b'], list(source))
        source.reset()
        assert_list_equal([1, 'a', 2, 3, 5, 4, 'b'], list(source))
