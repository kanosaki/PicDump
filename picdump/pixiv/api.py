
from picdump.webadapter import WebAdapter

class API:
    def __init__(self, adapter=None):
        self.adapter = adapter or WebAdapter()
        self.ranking = Ranking(self)
        self.search = Search(self)


# Enums
class RankingContentType:
    all = 'all'
    original = 'original'
    female = 'female'
    male = 'male'
    rookie = 'rookie'


class RankingSpan:
    daily = 'daily'
    weekly = 'weekly'
    monthly = 'monthly'


class SearchMode:
    by_tag = 's_tag'
    by_tag_full = 's_tag_full'
    by_keyword = 's_tc'  # tc = Title and Caption


# Config Facades
class Ranking:
    def __init__(self, api):
        self.api = api

    def __call__(self, span=None, content=):
        pass


class Search:
    def __init__(self, api):
        self.api = api

    def __call__(self, query=None):
        pass
