from picdump import pixiv
from picdump.utils import cached_property


class Pixiv:
    def __init__(self):
        self.pixiv = pixiv.create()
        self.pixiv.api.set_cache_dir('pixiv_cache')

    @cached_property
    def daily(self):
        return self.pixiv.ranking(self.pixiv.span.daily)

    def fetch_ranking(self):
        return self.daily.take()

    def sample_image(self):
        items = self.fetch_ranking()
        for item in items:
            if type(item).__name__ == 'Illust':
                return item
        return items[0]



