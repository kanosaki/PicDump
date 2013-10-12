import os
import os.path

# Utility functions
def cached_property(f):
    def get(self):
        try:
            return self._property_cache[f]
        except AttributeError:
            self._property_cache = {}
            x = self._property_cache[f] = f(self)
            return x
        except KeyError:
            x = self._property_cache[f] = f(self)
            return x
    return property(get)


def void_fn(*args, **kw):
    pass


def id_fn(arg):
    return arg


def constant_fn(const):
    def inner(*args, **kw):
        return const
    return inner


DEFAULT_TIMESTAMP_FORMAT = "%Y/%m/%d %H:%M:%S"


def format_datetime(stamp, fmt=DEFAULT_TIMESTAMP_FORMAT):
    return stamp.strftime(fmt)


APP_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../'))


def absjoin(*args):
    return os.path.abspath(os.path.join(*args))


def app_path(*args):
    if os.path.isabs(os.path.join(*args)):
        return os.path.join(*args)
    else:
        return absjoin(APP_ROOT, *args)


def remove_files(directory):
    if not os.path.isdir(directory):
        raise RuntimeError(directory + 'is not valid directory path')
    for file_name in os.listdir(directory):
        path = os.path.join(directory, file_name)
        if os.path.isfile(path):
            os.unlink(path)


