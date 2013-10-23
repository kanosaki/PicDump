import unittest
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


class TestCyclic(unittest.TestCase):
    def test_cyclic_spec(self):
        src_a = src(['A', 'B', 'C', 'D'])
        src_b = src([1, 2, 3])
        src_c = src(['a'])
        src_d = src([])
        source = conduit.cyclic(src_a, src_b, src_c, src_d)
        source_spec(source)

    def test_cyclic_reset(self):
        src_a = src(['A', 'B', 'C', 'D'])
        src_b = src([1, 2, 3])
        src_c = src(['a'])
        src_d = src([])
        source = conduit.cyclic(src_a, src_b, src_c, src_d)
        self.assertListEqual(['A', 1, 'a', 'B', 2, 'C', 3, 'D'], list(source))
        source.reset()
        source_spec(source)
        source.reset()
        self.assertListEqual(['A', 1, 'a', 'B', 2, 'C', 3, 'D'], list(source))

    def test_cyclic_basic(self):
        src_a = src(['A', 'B', 'C', 'D'])
        src_b = src([1, 2, 3])
        src_c = src(['a'])
        src_d = src([])
        source = conduit.cyclic(src_a, src_b, src_c, src_d)
        self.assertListEqual(['A', 1, 'a', 'B', 2, 'C', 3, 'D'], list(source))

    def test_cyclic_empty(self):
        source = conduit.cyclic(src([]))
        self.assertListEqual([], list(source))


class TestUnique(unittest.TestCase):
    def test_cyclic_basic(self):
        src_and_expected = [
            ([], []),
            ([1, 2, 3], [1, 2, 3]),
            ([1, 2, 2, 1], [1, 2]),
            ([None, None, None, 1], [None, 1]),
        ]
        for (s, e) in src_and_expected:
            source = src(s)
            self.assertListEqual(e, list(conduit.unique(source)))

    def test_reset(self):
        first = src([1, 2, 3, 3, 2, 1])
        unique = conduit.unique(first)
        self.assertEqual(1, next(unique))
        self.assertEqual(2, next(unique))
        self.assertEqual(3, next(unique))
        unique.reset()
        self.assertEqual(1, next(unique))
        self.assertEqual(2, next(unique))
        self.assertEqual(3, next(unique))
        with self.assertRaises(StopIteration):
            self.assertEqual(3, next(unique))

    def test_spec(self):
        first = src([1, 2, 3, 3, 2, 1])
        unique = conduit.unique(first)
        source_spec(unique)


def source_spec(source):
    """Test common source requirements."""
    # 'reset' check
    assert len(list(source)) != 0
    utils.assert_empty_iterator(source)
    source.reset()
    utils.assert_nonempty_iterator(source)
