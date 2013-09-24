
import queue
import urllib.parse
import copy


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


class PageIterator:
    def __init__(self, source):
        self.source = source
        self.queue = queue.Queue()
        self.is_source_empty = False

    def __next__(self):
        self.prefetch(1)
        try:
            return self.queue.get_nowait()
        except queue.Empty:
            raise StopIteration()

    def __iter__(self):
        return self

    def fetch(self):
        try:
            next_page = next(self.source)
            for item in next_page:
                self.queue.put(item)
        except StopIteration:
            self.is_source_empty = True

    def prefetch(self, buffer_to):
        if self.buffered_size < buffer_to and not self.is_source_empty:
            self.fetch()
            self.prefetch(buffer_to)

    @property
    def page_size(self):
        return 50

    @property
    def buffered_size(self):
        return self.queue.qsize()  # TODO: check validity.
                                   # qsize method basically returns approximate
                                   # size


def with_prefix(prefix, value):
    if value.startswith(prefix):
        return value
    else:
        return prefix + value


class URLBuilder:
    DEFAULT_PARTS = {
        'scheme': 'http',
        'host': '',
        'path': '',
        'params': {},
        'fragment': ''
    }
    _parts = None

    def __init__(self, **parts_kw):
        object.__setattr__(self, '_frozen', False)
        for k, v in parts_kw.items():
            if k not in self.DEFAULT_PARTS:
                raise ValueError('{} is not allowed'.format(k))
        parts = copy.deepcopy(self.DEFAULT_PARTS)
        parts.update(parts_kw)
        parts['path'] = with_prefix('/', parts['path'])
        parts['fragment'] = with_prefix('#', parts['fragment'])
        self._parts = parts
        self._frozen = True

    def update_with(self, **parts_kw):
        for k, v in parts_kw.items():
            if k not in self.DEFAULT_PARTS:
                raise ValueError('{} is not allowed'.format(k))
        newparts = copy.deepcopy(self._parts)
        newparts.update(parts_kw)
        return type(self)(**newparts)

    def __getattr__(self, key):
        if key not in self.DEFAULT_PARTS:
            raise ValueError('{} is not allowed'.format(key))
        return self._parts[key]

    def __hasattr__(self, key):
        return key in self.DEFAULT_PARTS

    @property
    def query(self):
        def mk_pair(kv):
            return '{}={}'.format(kv[0],
                                  urllib.parse.quote(str(kv[1]), safe=''))
        pairs = map(mk_pair, self.params.items())
        return '?' + '&'.join(pairs)

    def __str__(self):
        return '{}://{}{}{}{}'.format(self.scheme,
                                      self.host,
                                      self.path,
                                      self.query,
                                      self.fragment)

    def copy(self):
        return copy.deepcopy(self)

    def __eq__(self, other):
        return str(self) == str(other)

    def __setattr__(self, name, value):
        if not self._frozen:
            object.__setattr__(self, name, value)
        else:
            raise TypeError('Cannot set name %r on object of type %s' % (
                            name, self.__class__.__name__))

    def to_request(self):
        pass
