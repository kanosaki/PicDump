
import os.path


# Inherit and set 'data' attribute
class Image:
    def save_to(self, path=None, dir=None, filename=None):
        if path is None and dir is None:
            raise RuntimeError('path or directory must be specified')
        if path:
            self.save_to_path(path)
        else:
            filename = filename or self.default_filename
            self.save_to_path(os.path.join(dir, filename))

    def save_to_path(self, path):
        with open(path, 'wb') as fp:
            fp.write(self.data)

    @property
    def default_filename(self):
        raise NotImplementedError()
