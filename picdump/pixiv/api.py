import datetime

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
        self.ranking_log = RankingLog(self)
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

    def mk_static_iterator(self, requrl):
        return PageIterator(StaticPageFetcher(self.api, requrl))

    mk_iterator = mk_static_iterator

    def mk_dynamic_iterator(self, url_factory):
        return PageIterator(DynamicPageFetcher(self.api, url_factory))


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


class RankingLog(APIFacade):
    path = '/iphone/ranking_log.php'

    def __call__(self, year, month, day, mode: RankingSpan=RankingSpan.daily):
        requrl = self.urlbuilder.update_with(
            params={
                'mode': mode,
                'Date_Year': year,
                'Date_Month': '{:02d}'.format(month),
                'Date_Day': '{:02d}'.format(day)
            }
        )
        return self.mk_iterator(requrl)

    def days_ago(self, days, mode: RankingSpan=RankingSpan.daily):
        delta = datetime.timedelta(days=days)
        factory = RankingLogTimedeltaFactory(self.urlbuilder, delta, mode)
        return self.mk_dynamic_iterator(factory)

    def yesterday(self):
        return self.days_ago(1)


class RankingLogTimedeltaFactory:
    def __init__(self, base_url, delta, mode):
        self.delta = delta
        self.mode = mode
        self.base_url = base_url

    def __call__(self):
        date = self.designate_date()
        return self.base_url.update_with(
            params={
                'mode': self.mode,
                'Date_Year': date.year,
                'Date_Month': '{:02d}'.format(date.month),
                'Date_Day': '{:02d}'.format(date.day)
            }
        )

    def designate_date(self):
        the_day = datetime.datetime.now() - self.delta
        return the_day.date()


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
    def __init__(self, api, begin_page=1):
        self.adapter = api.adapter
        self.api = api
        self.current_page = begin_page

    def get_next_urlbuilder(self):
        raise NotImplementedError()

    def __next__(self):
        builder = self.get_next_urlbuilder()
        url = builder.update_params(p=self.current_page)
        self.current_page += 1
        csv_page = self.adapter.get_text(url)
        contents = [i for i in csv.parse(csv_page, self.api) if i.is_valid]
        if len(contents) == 0:
            raise StopIteration()
        return contents

    def reset(self):
        self.current_page = 1


class StaticPageFetcher(PageFetcher):
    def __init__(self, api, urlbuilder, begin_page=1):
        super().__init__(api, begin_page)
        self.urlbuilder = urlbuilder

    def get_next_urlbuilder(self):
        return self.urlbuilder


class DynamicPageFetcher(PageFetcher):
    def __init__(self, api, url_factory, begin_page=1):
        super().__init__(api, begin_page)
        self.url_factory = url_factory

    def get_next_urlbuilder(self):
        return self.url_factory()
