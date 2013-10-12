import shutil
import os.path
from picdump.utils import normalize_filename


# Inherit and set 'data' attribute
class Image:
    def __init__(self):
        self.saved_path = None

    def save_to(self, path=None, dir=None, filename=None, force=False):
        if path is None and dir is None:
            raise RuntimeError('path or directory must be specified')
        if path:
            self.save_to_path(path, force)
        else:
            filename = normalize_filename(filename or self.default_filename)
            self.save_to_path(os.path.join(dir, filename), force)

    def save_to_path(self, path, force):
        if self.saved_path and not force:
            self.copy_to(path)
            return
        with open(path, 'wb') as fp:
            fp.write(self.data)
        self.saved_path = path

    def copy_to(self, path):
        if self.saved_path == path:
            return
        shutil.copyfile(self.saved_path, path)

    @property
    def default_filename(self):
        raise NotImplementedError()
