from picdump.pixiv.item import Item
from picdump.utils import cached_property
from picdump.pixiv.image import Image


class Illust(Item):
    @cached_property
    def image_url(self):
        filename = "{}.{}".format(self.item_id, self.extension)
        return self.user_image_url(filename)

    def open_image(self):
        referer = self.member_illust_page_url
        res = self.api.adapter.get(self.image_url, referer=referer)
        return Image(res, self)

    def open_all_images(self):
        return [self.open_image()]

    @property
    def is_illust(self):
        return True



