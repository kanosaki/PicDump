import unittest
import os
import shutil

import utils


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


