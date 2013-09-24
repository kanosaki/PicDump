import unittest
import itertools

import picdump.utils as utl


class TestUtilFunctions(unittest.TestCase):
    def test_id_fn(self):
        values = [1, "foo", object(), [], {}]
        for v in values:
            self.assertEqual(v, utl.id_fn(v))

    def test_void_fn(self):
        values = [1, "foo", object(), [], {}]
        for v in values:
            self.assertEqual(None, utl.void_fn(v))

        self.assertEqual(None, utl.void_fn(None, None, None))
        self.assertEqual(None, utl.void_fn(None, 1, 2, 3, hoge="fuga"))

    def test_constant_fn(self):
        const = "foo"
        const_fn = utl.constant_fn(const)
        values = [1, "foo", object(), [], {}]
        for v in values:
            self.assertEqual(const, const_fn(v))


class TestPageIterator(unittest.TestCase):
    def test_empty(self):
        source = iter([])
        pi = utl.PageIterator(source)
        self.assertEqual(list(pi), [])

    def test_full_page_fetching(self):
        pages = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
        pi = utl.PageIterator(iter(pages))
        self.assertEqual(list(pi), [elem for page in pages for elem in page])
        self.assertTrue(pi.is_source_empty)

    def test_partial_page_fetching(self):
        pages = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
        pi = utl.PageIterator(iter(pages))
        taken = list(itertools.islice(pi, 4))
        self.assertFalse(pi.is_source_empty)
        self.assertEqual(taken, [1, 2, 3, 4])
        self.assertEqual(pi.buffered_size, 2)
        pi.prefetch(2)
        self.assertEqual(pi.buffered_size, 2)
        pi.prefetch(3)
        self.assertEqual(pi.buffered_size, 5)
        self.assertEqual(list(pi), [5, 6, 7, 8, 9])
        self.assertTrue(pi.is_source_empty)


class TestURLBuilder(unittest.TestCase):
    def test_init(self):
        builder = utl.URLBuilder(scheme="http",
                                 host="www.example.com",
                                 path="/some/path",
                                 params={'bar': ' '},
                                 fragment="frg")
        expected = "http://www.example.com/some/path?bar=%20#frg"
        self.assertEqual(str(builder), expected)
        builder2 = builder.update_with('host', 'www.example2.com')
        expected = "http://www.example2.com/some/path?bar=%20#frg"
        self.assertEqual(str(builder2), expected)

    def test_immutability(self):
        builder = utl.URLBuilder(scheme="http",
                                 host="www.example.com",
                                 path="/some/path",
                                 params={'bar': ' '},
                                 fragment="frg")
        builder0 = builder.update_with('host', 'www.example.com')
        builder2 = builder.update_with('host', 'www.example2.com')
        self.assertTrue(builder is not builder2)
        self.assertTrue(builder is not builder0)
        self.assertNotEqual(builder, builder2)
        self.assertEqual(builder, builder0)
        with self.assertRaises(TypeError):
            builder.path = 'foobar'

    def test_query(self):
        builder = utl.URLBuilder(scheme="http",
                                 host="www.example.com",
                                 path="/some/path",
                                 params={'bar': ' ', 'foo': 1},
                                 fragment="frg")
        self.assertIn(builder.query, set(['?bar=%20&foo=1', '?foo=1&bar=%20']))

    def test_with_prefix(self):
        self.assertEqual('/hoge/fuga', utl.with_prefix('/', 'hoge/fuga'))
        self.assertEqual('/hoge/fuga', utl.with_prefix('/', '/hoge/fuga'))
