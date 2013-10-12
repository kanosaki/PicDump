
import os.path


class Image:
    def save_to(self, path=None, directory=None, filename=None):
        if path is None and dir is None:
            raise RuntimeError('path or directory must be specified')
        if path:
            self.save_to_path(path)
        else:
            filename = filename or self.default_filename
            self.save_to_path(os.path.join(directory, filename))

    def save_to_path(self, path):
        with open(path, 'wb') as fp:
            fp.write(self.data)

    @property
    def default_filename(self):
        raise NotImplementedError()

    @property
    def data(self):
        raise NotImplementedError()
