
# PATH adjust
import sys
import os


def _absjoin(*args):
    return os.path.abspath(os.path.join(*args))


APP_ROOT = _absjoin(os.path.dirname(__file__), "..")
sys.path.insert(0, APP_ROOT)

from picdump.app import App
from picdump.config import ConfigLoader

# Boot configuration
DEFAULT_CONFIG = _absjoin(APP_ROOT, "config.py")


def main():
    with open(DEFAULT_CONFIG) as fp_config:
        config_string = fp_config.read()
        loader = ConfigLoader(config_string)
        config = loader.load()
    app = App(config)
    app.start()


if __name__ == '__main__':
    main()
