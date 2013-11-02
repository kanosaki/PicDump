import os
import shutil

from nose.tools import *

utils = __import__('utils')


class TestTestUtils:
    def test_path_from_test(self):
        base_path = os.path.abspath(os.path.join(os.path.dirname(__file__)))
        assert_equal(base_path, utils.TEST_DIR)
        assert_equal(os.path.join(base_path, "foobar"), utils.path_from_test("foobar"))


class TestTempDir:
    def setUp(self):
        self.target_dir = utils.path_from_test('sample_dir')
        if os.path.exists(self.target_dir):
            shutil.rmtree(self.target_dir)

    def test_setup(self):
        target_dir = self.target_dir
        assert_false(os.path.exists(target_dir))
        with utils.TempDir('sample_dir') as d:
            with d.open('foobar', 'w') as f:
                f.write('hogehoge')
            ok_(os.path.isfile(utils.absjoin(target_dir, 'foobar')))
            ok_(os.path.exists(target_dir))
        assert_false(os.path.exists(target_dir))
        assert_false(os.path.isfile(utils.absjoin(target_dir, 'foobar')))

    def test_delete_if_exists_and_nesting(self):
        target_dir = self.target_dir
        assert_false(os.path.exists(target_dir))
        with utils.TempDir('sample_dir') as d:
            with utils.TempDir('sample_dir', delete_if_exists=True) as dd:
                pass
            assert_false(os.path.isfile(utils.absjoin(target_dir, 'foobar')))
            assert_false(os.path.exists(target_dir))
            with assert_raises(IOError):
                with d.open('foobar', 'w') as f:
                    f.write('hogehoge')

    def test_already_exists(self):
        target_dir = self.target_dir
        assert_false(os.path.exists(target_dir))
        with utils.TempDir('sample_dir') as d:
            with d.open('foobar', 'w') as f:
                f.write('hogehoge')
            with assert_raises(IOError):
                with utils.TempDir('sample_dir') as dd:
                    pass
            ok_(os.path.isfile(utils.absjoin(target_dir, 'foobar')))
            ok_(os.path.exists(target_dir))
        assert_false(os.path.exists(target_dir))
        assert_false(os.path.isfile(utils.absjoin(target_dir, 'foobar')))


class TestIteratorAssertions:
    def test_empty(self):
        with assert_raises(AssertionError):
            utils.assert_empty_iterator(iter([1]))
        utils.assert_empty_iterator(iter([]))

    def test_nonempty(self):
        with assert_raises(AssertionError):
            utils.assert_nonempty_iterator(iter([]))
        utils.assert_nonempty_iterator(iter([1]))




