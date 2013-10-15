
# Utils for testing

import os
import shutil

TEST_MODE = os.environ.get('UNITTEST_MODE')


def absjoin(*path):
    return os.path.abspath(os.path.join(*path))


TEST_DIR = absjoin(os.path.dirname(__file__))


def path_from_test(*path):
    return absjoin(TEST_DIR, *path)


class TempDir:
    def __init__(self, *path, delete_if_exists=False):
        self.path = path_from_test(*path)
        self.delete_if_exists = delete_if_exists

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.teardown()

    def __enter__(self):
        self.setup()
        return self

    def open(self, path, mode='r'):
        return open(absjoin(self.path, path), mode)

    def setup(self):
        if os.path.exists(self.path):
            if self.delete_if_exists:
                shutil.rmtree(self.path)
            else:
                raise RuntimeError('File exists')
        if not os.path.isdir(self.path):
            os.makedirs(self.path)

    def teardown(self):
        shutil.rmtree(self.path)
