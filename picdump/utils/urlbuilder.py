
import urllib.parse
import copy


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

    def update_params(self, **kw):
        newparams = copy.deepcopy(self.params)
        newparams.update(kw)
        return self.update_with(params=newparams)

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
        raise NotImplemented()
