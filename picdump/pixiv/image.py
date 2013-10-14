from urllib.parse import urlparse

from picdump import image


class ItemImage(image.Image):
    def __init__(self, item, api, content_factory):
        super().__init__()
        self.item = item
        self.api = api
        self.content_factory = content_factory

    @property
    def default_filename(self):
        item = self.item
        return '{}{} {}{}'.format(item.item_id, self.type_suffix, item.title, self.dot_and_extension)

    @property
    def saved_path(self):
        cache = self.api.cache
        if self.cache_id in cache:
            return cache.get_path(self.cache_id)
        else:
            return None

    def fetch_content(self):
        content = self.content_factory()
        self.api.cache.put(self.cache_id, content)
        return content

    @property
    def dot_and_extension(self):
        return '.{}'.format(self.item.extension)


class IllustBigImage(ItemImage):
    type_suffix = ''

    @property
    def cache_id(self):
        return '{}.{}'.format(self.item.item_id, self.item.extension)


class IllustMobileImage(ItemImage):
    type_suffix = '_mobile'

    @property
    def dot_and_extension(self):
        return '.jpg'

    @property
    def cache_id(self):
        return '{}_480mw.jpg'.format(self.item.item_id)


class ThumbnailImage(ItemImage):
    type_suffix = '_thumb'

    @property
    def dot_and_extension(self):
        return '.jpg'

    @property
    def cache_id(self):
        return '{}_128x128.jpg'.format(self.item.item_id)


class MangaPageImage(ItemImage):
    def __init__(self, item, api, content_factory, page):
        super().__init__(item, api, content_factory)
        self.page = page

    @property
    def cache_id(self):
        return '{}_p{}.{}'.format(self.item.item_id, self.page, self.item.extension)

    @property
    def type_suffix(self):
        return '_p{}'.format(self.page)


class MemberThumbnail(ItemImage):
    type_suffix = '_member_thumb'

    @property
    def default_filename(self):
        item = self.item
        return '{} {}.jpg'.format(item.author_id, item.author_screen_name)

    @property
    def dot_and_extension(self):
        return '.jpg'

    @property
    def cache_id(self):
        return '{}_80.jpg'.format(self.item.author_id)
