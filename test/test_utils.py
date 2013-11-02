import itertools

from nose.tools import *

import picdump.utils as utl


class TestUtilFunctions:
    def test_id_fn(self):
        values = [1, "foo", object(), [], {}]
        for v in values:
            assert_equal(v, utl.id_fn(v))

    def test_void_fn(self):
        values = [1, "foo", object(), [], {}]
        for v in values:
            assert_equal(None, utl.void_fn(v))

        assert_equal(None, utl.void_fn(None, None, None))
        assert_equal(None, utl.void_fn(None, 1, 2, 3, hoge="fuga"))

    def test_constant_fn(self):
        const = "foo"
        const_fn = utl.constant_fn(const)
        values = [1, "foo", object(), [], {}]
        for v in values:
            assert_equal(const, const_fn(v))


class TestPageIterator:
    def test_empty(self):
        source = iter([])
        pi = utl.PageIterator(source)
        assert_equal(list(pi), [])
        with assert_raises(StopIteration):
            source = iter([])
            pi = utl.PageIterator(source)
            next(pi)

    def test_full_page_fetching(self):
        pages = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
        pi = utl.PageIterator(iter(pages))
        assert_equal(list(pi), [elem for page in pages for elem in page])
        assert_true(pi.is_source_empty)

    def test_partial_page_fetching(self):
        pages = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
        pi = utl.PageIterator(iter(pages))
        taken = list(itertools.islice(pi, 4))
        assert_false(pi.is_source_empty)
        assert_equal(taken, [1, 2, 3, 4])
        assert_equal(pi.buffered_size, 2)
        pi.prefetch(2)
        assert_equal(pi.buffered_size, 2)
        pi.prefetch(3)
        assert_equal(pi.buffered_size, 5)
        assert_equal(list(pi), [5, 6, 7, 8, 9])
        assert_true(pi.is_source_empty)


class TestURLBuilder:
    def test_init(self):
        builder = utl.URLBuilder(scheme="http",
                                 host="www.example.com",
                                 path="/some/path",
                                 params={'bar': ' '},
                                 fragment="frg")
        expected = "http://www.example.com/some/path?bar=%20#frg"
        assert_equal(str(builder), expected)
        builder2 = builder.update_with(host='www.example2.com')
        expected = "http://www.example2.com/some/path?bar=%20#frg"
        assert_equal(str(builder2), expected)

    def test_immutability(self):
        builder = utl.URLBuilder(scheme="http",
                                 host="www.example.com",
                                 path="/some/path",
                                 params={'bar': ' '},
                                 fragment="frg")
        builder0 = builder.update_with(host='www.example.com')
        builder2 = builder.update_with(host='www.example2.com')
        assert_true(builder is not builder2)
        assert_true(builder is not builder0)
        assert_not_equal(builder, builder2)
        assert_equal(builder, builder0)
        with assert_raises(TypeError):
            builder.path = 'foobar'

    def test_query(self):
        builder = utl.URLBuilder(scheme="http",
                                 host="www.example.com",
                                 path="/some/path",
                                 params={'bar': ' ', 'foo': 1},
                                 fragment="frg")
        assert_in(builder.query, set(['?bar=%20&foo=1', '?foo=1&bar=%20']))

    def test_with_prefix(self):
        assert_equal('/hoge/fuga', utl.with_prefix('/', 'hoge/fuga'))
        assert_equal('/hoge/fuga', utl.with_prefix('/', '/hoge/fuga'))
