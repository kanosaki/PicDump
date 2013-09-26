
from picdump.webadapter import WebAdapter
from picdump.utils import URLBuilder, PageIterator
from picdump.pixiv import csv


API_HOST = "spapi.pixiv.net"


class API:
    def __init__(self, adapter=None):
        self.adapter = adapter or WebAdapter()
        self.ranking = Ranking(self)
        self.search = Search(self)


# ---------------------------------
# Enums
# ---------------------------------
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


# ---------------------------------
# Config Facades
# ---------------------------------

class APIFacade:
    def __init__(self, api):
        self.api = api
        self.urlbuilder = URLBuilder(
            host=API_HOST,
            path=self.path
        )

    @property
    def path(self):
        raise NotImplemented()

    def mk_iterator(self, requrl):
        return PageIterator(PageFetcher(self.api.adapter, requrl))


class Ranking(APIFacade):
    path = '/iphone/ranking.php'

    def __call__(self, span, content=RankingContentType.all):
        requrl = self.urlbuilder.update_with(
            params={
                'mode': span,
                'content': content
            }
        )
        return self.mk_iterator(requrl)


class Search(APIFacade):
    path = '/iphone/search.php'

    def __call__(self, query, mode=SearchMode.by_tag):
        requrl = self.urlbuilder.update_with(
            params={
                'word': query,
                's_mode': mode
            }
        )
        return self.mk_iterator(requrl)


# ---------------------------------
# Utilities
# ---------------------------------
class PageFetcher:
    def __init__(self, adapter, urlbuilder, begin_page=1):
        self.adapter = adapter
        self.current_page = begin_page
        self.urlbuilder = urlbuilder

    def __next__(self):
        url = self.urlbuilder.update_params(p=self.current_page)
        self.current_page += 1
        with self.adapter.open(url) as f:
            return csv.read(f)
