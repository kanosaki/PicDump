import shutil
from picdump.utils import normalize_filename, absjoin


# Inherit and set 'content' attribute
class Image:
    def __init__(self):
        self._saved_path = None

    @property
    def saved_path(self):
        return self._saved_path

    @property
    def is_fetched(self):
        return self.saved_path is not None

    def save_to(self, path=None, dir=None, filename=None, force=False):
        save_path = self.determine_save_path(path=path, dir=dir, filename=filename)
        if self.is_fetched and not force:
            self.copy_file_to(save_path)
        else:
            data = self.fetch_content()
            self.write_to(save_path, data)

    def determine_save_path(self, path=None, dir=None, filename=None):
        if path is None and dir is None:
            raise RuntimeError('path or directory must be specified')
        if not path:
            filename = normalize_filename(filename or self.default_filename)
            path = absjoin(dir, filename)
        return path

    def write_to(self, path, data):
        with open(path, 'wb') as fp:
            fp.write(data)

    def copy_file_to(self, path):
        if self.saved_path == path:
            return
        shutil.copyfile(self.saved_path, path)

    @property
    def default_filename(self):
        raise NotImplementedError()
