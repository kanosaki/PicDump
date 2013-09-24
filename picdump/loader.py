
import os.path

import picdump.config


def _absjoin(*args):
    return os.path.abspath(os.path.join(*args))


APP_ROOT = _absjoin(os.path.dirname(__file__), "..")
DEFAULT_CONFIG = _absjoin(APP_ROOT, "config.py")


class Loader:
    def __init__(self, confpath=DEFAULT_CONFIG):
        self.confpath = confpath
        self.config(confpath)

    def config(self, confpath):
        with open(confpath) as f:
            confloader = self.create_configloader(f)
            return confloader.load()

    def create_configloader(self, f):
        return picdump.config.ConfigLoader(f)

    def craete_app(self):
        pass
