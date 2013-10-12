import re
from html.parser import HTMLParser
from datetime import datetime

from picdump.utils import cached_property, format_datetime
from picdump.pixiv.image import Image

_html_parser = HTMLParser()
TIMESTAMP_FORMAT = '%Y-%m-%d %H:%M:%S'


def unescape(html_doc):
    """
    Unescape html entity.

    For example: unescape('foo&lt;bar') -> 'foo<bar'
    :param html_doc: HTML entity escaped string
    :return: unescaped plain string.
    """
    return _html_parser.unescape(html_doc)


class Item:
    def __init__(self, row, api):
        self._row = row
        self.api = api

    @property
    def is_accessible(self):
        return self.item_id != 0

    @cached_property
    def item_id(self):
        return int(self._row.illust_id)

    # An alias for item_id
    @property
    def illust_id(self):
        return self.item_id

    @cached_property
    def author_id(self):
        return int(self._row.author_id)

    @property
    def extension(self):
        return self._row.extension

    @property
    def title(self):
        return self._row.title

    @property
    def server(self):
        return self._row.server

    @property
    def author_screen_name(self):
        return self._row.author_screen_name

    @property
    def thumbnail(self):
        return self._row.thumbnail

    def open_thumbnail(self):
        res = self.api.adapter.get(self.thumbnail)
        return Image(res, self, type_prefix='thumb')

    @property
    def mobile_image(self):
        return self._row.mobile_image

    @cached_property
    def timestamp(self):
        return datetime.strptime(self._row.timestamp, TIMESTAMP_FORMAT)

    @cached_property
    def tags(self):
        return [unescape(tag) for tag in self._row.tags.split(' ')]

    @cached_property
    def tools(self):
        return [unescape(tool) for tool in self._row.tools.split(' ')]

    @cached_property
    def comments(self):
        return int(self._row.comments)

    @cached_property
    def points(self):
        return int(self._row.points)

    @cached_property
    def views(self):
        return int(self._row.views)

    @cached_property
    def caption(self):
        return unescape(self._row.caption)

    @cached_property
    def pages(self):
        try:
            return int(self._row.pages)
        except ValueError:  # A manga does not have page
            return None

    @property
    def author_name(self):
        return self._row.author_name

    @property
    def author_thumbnail(self):
        return self._row.author_thumbnail

    def open_author_thumbnail(self):
        res = self.api.adapter.get(self.author_thumbnail)
        return Image(res, self, type_prefix='author_thumb')

    def __str__(self):
        classname = type(self).__name__
        return '[{} "{}"(by {}) id={} time={}]'.format(classname,
                                                       self.title,
                                                       self.author_name,
                                                       self.item_id,
                                                       format_datetime(self.timestamp))

    __repr__ = __str__

    PAT_USER_IMAGE_DIRECTORY_TRIMMER = re.compile(r'/mobile/.+')

    def user_image_url(self, filename):
        pat = self.PAT_USER_IMAGE_DIRECTORY_TRIMMER
        return pat.sub('/' + filename, self.mobile_image)

    @property
    def member_illust_page_url(self):
        return 'http://www.pixiv.net/member_illust.php?mode=medium&illust_id={}'.format(self.item_id)
