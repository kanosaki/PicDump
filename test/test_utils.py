
from nose.tools import assert_equals

import picdump.utils as utl


class TestUtilFunctions:
    def test_id_fn(self):
        values = [1, "foo", object(), [], {}]
        for v in values:
            assert_equals(v, utl.id_fn(v))

    def test_void_fn(self):
        values = [1, "foo", object(), [], {}]
        for v in values:
            assert_equals(None, utl.void_fn(v))

        assert_equals(None, utl.void_fn(None, None, None))
        assert_equals(None, utl.void_fn(None, 1, 2, 3, hoge="fuga"))

    def test_constant_fn(self):
        const = "foo"
        const_fn = utl.constant_fn(const)
        values = [1, "foo", object(), [], {}]
        for v in values:
            assert_equals(const, const_fn(v))
