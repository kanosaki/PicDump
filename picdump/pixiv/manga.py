from picdump.pixiv.item import Item
from picdump.utils import cached_property
from picdump.pixiv.image import Image


class Manga(Item):
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
            res = self.api.adapter.get(url, referer=referer)
            yield Image(res, self, type_prefix=str(page))

    def open_all_images(self):
        return list(self.open_page_images())

    def open_image(self):
        referer = self.member_illust_page_url
        res = self.api.adapter.get(self.page_urls[0], referer=referer)
        return Image(res, self)

    @property
    def is_manga(self):
        return True
