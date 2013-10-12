from picdump.pixiv.item import Item

from picdump.utils import cached_property


class Illust(Item):
    @cached_property
    def image_url(self):
        filename = "{}.{}".format(self.item_id, self.extension)
        return self.user_image_url(filename)


