import os

from picdump.webadapter import WebAdapter
from picdump.utils import URLBuilder, PageIterator, app_path
from picdump.pixiv import csv
from picdump.pixiv import cache
from picdump import app


API_HOST = "spapi.pixiv.net"


class API(app.HasAppMixin):
    def __init__(self, adapter=None):
        super().__init__()
        self.adapter = adapter or WebAdapter()
        self.ranking = Ranking(self)
        self.search = Search(self)
        self.cache = cache.VoidCache()

    def image_cache_dir(self):
        config = self.app.config
        return app_path(config.cache_dir, 'pixiv')

    def on_app_injected(self, app):
        self.cache = cache.ImageCache(self.image_cache_dir())

    def set_cache_dir(self, dirpath):
        self.cache = cache.ImageCache(dirpath)


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
        return PageIterator(PageFetcher(self.api, requrl))


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
    def __init__(self, api, urlbuilder, begin_page=1):
        self.adapter = api.adapter
        self.api = api
        self.current_page = begin_page
        self.urlbuilder = urlbuilder

    def __next__(self):
        url = self.urlbuilder.update_params(p=self.current_page)
        self.current_page += 1
        csv_page = self.adapter.get_text(url)
        contents = list(csv.parse(csv_page, self.api))
        if len(contents) == 0:
            raise StopIteration()
        return contents

    def reset(self):
        self.current_page = 1
