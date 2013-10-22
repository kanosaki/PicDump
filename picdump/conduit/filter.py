

class FilterBase:
    def predicate(self, obj):
        pass

    def __and__(self, other):
        return ConjunctionFilter(self, other)

    def __or__(self, other):
        return DisjunctionFilter(self, other)

    def reset(self):
        raise NotImplementedError()


class CompositeFilter(FilterBase):
    def __init__(self, *children):
        self.children = children

    def reset(self):
        for child in self.children:
            child.reset()


class ConjunctionFilter(CompositeFilter):
    def __and__(self, other):
        self.children.append(other)
        return self

    def predicate(self, obj):
        for child in self.children:
            if not child.predicate(obj):
                return False
        return True

    def __call__(self, obj):
        return self.predicate(obj)

    def __str__(self):
        return '({})'.format(' and '.join(self.children))


class DisjunctionFilter(CompositeFilter):
    def __or__(self, other):
        self.children.append(other)
        return self

    def predicate(self, obj):
        for child in self.children:
            if child.predicate(obj):
                return True
        return False

    def __str__(self):
        return '({})'.format(' or '.join(self.children))


class BlacklistFilter(FilterBase):
    pass


class WhitelistFilter(FilterBase):
    pass


class PassFilter(FilterBase):
    def predicate(self, obj):
        return True


PassFilter.default = PassFilter()


class SizeFilter(FilterBase):
    def __init__(self, limit):
        self.passed = 0
        if limit < 0:
            raise ValueError('Negative number is not allowed.')
        self.limit = limit

    def predicate(self, obj):
        if self.passed >= self.limit:
            return False
        else:
            self.passed += 1
            return True

    def reset(self):
        self.passed = 0

