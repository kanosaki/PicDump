import os

from picdump import utils


class ImageCache:
    def __init__(self, cache_dir):
        if not os.path.isdir(cache_dir):
            os.makedirs(cache_dir)
        self.cache_dir = cache_dir

    def get_path(self, cache_id):
        return utils.absjoin(self.cache_dir, utils.normalize_filename(cache_id))

    def __contains__(self, cache_id):
        return os.path.isfile(self.get_path(cache_id))

    def get(self, cache_id):
        path = self.get_path(cache_id)
        with open(path, 'rb') as f:
            return f.read()

    def put(self, cache_id, content):
        path = self.get_path(cache_id)
        with open(path, 'wb') as f:
            f.write(content)


class VoidCache:
    def __contains__(self, item):
        return False

    def put(self, cache_id, content):
        pass

    def get_path(self, cache_id):
        raise RuntimeError('Cache system has not initialized yet.')

    def get(self, cache_id):
        raise RuntimeError('Cache system has not initialized yet.')


