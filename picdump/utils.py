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
