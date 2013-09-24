
import queue
import urllib.parse


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
    def __init__(self, scheme='http',
                 host='',
                 path='',
                 params={},
                 fragment=None):
        self._path = self._fragment = ''
        self.scheme = scheme
        self.host = host
        self.path = path
        self.params = params
        self.fragment = fragment

    @property
    def path(self):
        return self._path

    @path.setter
    def path(self, value):
        self._path = with_prefix('/', value)

    @property
    def fragment(self):
        return self._fragment

    @fragment.setter
    def fragment(self, value):
        self._fragment = with_prefix('#', value)

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

    def to_request(self):
        pass
