
__all__ = ['filter_manga']

from picdump.conduit import filter


class MangaFilter(filter.BlacklistFilter):
    def check(self, obj):
        return not obj.is_manga

    def pre_check(self, obj):
        return hasattr(obj, 'is_manga')


filter_manga = MangaFilter
