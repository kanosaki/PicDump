from picdump.pixiv.item import Item
from picdump.utils import cached_property
from picdump.pixiv import image


class Manga(Item):
    def _open_manga_page(self, url, page, referer=None):
        api = self.api

        def factory():
            res = api.adapter.get(url, referer=referer)
            res.raise_for_status()
            return res.content
        return image.MangaPageImage(self, self.api, factory, page)

    @cached_property
    def page_urls(self):
        filenames = (
            '{}_p{}.{}'.format(self.item_id, page, self.extension)
            for page in range(self.pages)
        )
        return list(map(self.user_image_url, filenames))

    def open_page_images(self):
        referer = self.member_illust_page_url
        for url, page in zip(self.page_urls, range(self.pages)):
            yield self._open_manga_page(url, page, referer)

    def open_all_images(self):
        return list(self.open_page_images())

    def open_image(self):
        referer = self.member_illust_page_url
        return self._open_manga_page(self.page_urls[0], 0, referer=referer)

    @property
    def is_manga(self):
        return True
