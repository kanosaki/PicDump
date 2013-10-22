import unittest
import os
import shutil

utils = __import__('utils')


class TestTestUtils(unittest.TestCase):
    def test_path_from_test(self):
        base_path = os.path.abspath(os.path.join(os.path.dirname(__file__)))
        self.assertEqual(base_path, utils.TEST_DIR)
        self.assertEqual(os.path.join(base_path, "foobar"), utils.path_from_test("foobar"))


class TestTempDir(unittest.TestCase):
    def setUp(self):
        self.target_dir = utils.path_from_test('sample_dir')
        if os.path.exists(self.target_dir):
            shutil.rmtree(self.target_dir)

    def test_setup(self):
        target_dir = self.target_dir
        self.assertFalse(os.path.exists(target_dir))
        with utils.TempDir('sample_dir') as d:
            with d.open('foobar', 'w') as f:
                f.write('hogehoge')
            self.assertTrue(os.path.isfile(utils.absjoin(target_dir, 'foobar')))
            self.assertTrue(os.path.exists(target_dir))
        self.assertFalse(os.path.exists(target_dir))
        self.assertFalse(os.path.isfile(utils.absjoin(target_dir, 'foobar')))

    def test_delete_if_exists_and_nesting(self):
        target_dir = self.target_dir
        self.assertFalse(os.path.exists(target_dir))
        with utils.TempDir('sample_dir') as d:
            with utils.TempDir('sample_dir', delete_if_exists=True) as dd:
                pass
            self.assertFalse(os.path.isfile(utils.absjoin(target_dir, 'foobar')))
            self.assertFalse(os.path.exists(target_dir))
            with self.assertRaises(IOError):
                with d.open('foobar', 'w') as f:
                    f.write('hogehoge')

    def test_already_exists(self):
        target_dir = self.target_dir
        self.assertFalse(os.path.exists(target_dir))
        with utils.TempDir('sample_dir') as d:
            with d.open('foobar', 'w') as f:
                f.write('hogehoge')
            with self.assertRaises(IOError):
                with utils.TempDir('sample_dir') as dd:
                    pass
            self.assertTrue(os.path.isfile(utils.absjoin(target_dir, 'foobar')))
            self.assertTrue(os.path.exists(target_dir))
        self.assertFalse(os.path.exists(target_dir))
        self.assertFalse(os.path.isfile(utils.absjoin(target_dir, 'foobar')))


class TestIteratorAssertions(unittest.TestCase):
    def test_empty(self):
        with self.assertRaises(AssertionError):
            utils.assert_empty_iterator(iter([1]))
        utils.assert_empty_iterator(iter([]))

    def test_nonempty(self):
        with self.assertRaises(AssertionError):
            utils.assert_nonempty_iterator(iter([]))
        utils.assert_nonempty_iterator(iter([1]))




