
from .base import Source


class FilterBase(Source):
    def predicate(self, obj):
        pass

    def reset(self):
        super().reset()

    def __next__(self):
        next_elem = next(self.parent)
        while not self.predicate(next_elem):
            next_elem = next(self.parent)
        return next_elem


class UniqueFilter(FilterBase):
    def __init__(self, parent=None):
        super().__init__(parent)
        self._history = set()

    def predicate(self, obj):
        is_newone = obj not in self._history
        if is_newone:
            self._history.add(obj)
        return is_newone

    def reset(self):
        self._history.clear()
        super().reset()


class DefaultedFilter(FilterBase):
    default_result = None

    def predicate(self, obj):
        if self.pre_check(obj) is True:
            try:
                return self.check(obj)
            except (AttributeError, NameError, KeyError):
                pass
        return self.default_result

    def check(self, obj):
        """Filter body. AttributeError, NameError and KeyError will be
           ignored and default_value will be returned."""

    def pre_check(self, obj):
        """Check whether it should be evaluated by this filter."""
        return True


class BlacklistFilter(DefaultedFilter):
    default_result = False


class WhitelistFilter(DefaultedFilter):
    default_result = True


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


