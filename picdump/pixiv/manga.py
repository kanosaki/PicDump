from picdump.pixiv.item import Item

from picdump.utils import cached_property


class Manga(Item):
    @cached_property
    def page_urls(self):
        filenames = (
            '{}_p{}.{}'.format(self.item_id, page, self.extension)
            for page in range(self.pages)
        )
        return list(map(self.user_image_url, filenames))

