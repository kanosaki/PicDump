
from urllib.parse import urlsplit

from picdump.pixiv.item import Item
from picdump.utils import cached_property
from picdump.pixiv import image

TIME_FRAGMENT_FORMAT = "%Y/%m/%d/%H/%M/%S"


class Illust(Item):
    @cached_property
    def image_url(self):
        # http://i1.pixiv.net/img-original/img/2014/12/14/20/55/07/47560048_p0.jpg
        time_fragment = self.created_at.strftime(TIME_FRAGMENT_FORMAT)
        return "http://{}/img-original/img/{}/{}_p0.{}".format(
            self.image_server,
            time_fragment,
            self.illust_id,
            self.extension)

    @property
    def image_server(self):
        splitted = urlsplit(self.mobile_image)
        return splitted.netloc

    def open_image(self):
        referer = self.member_illust_page_url
        print(self.image_url)
        return self._open(self.image_url, image.IllustBigImage, referer=referer)

    def open_all_images(self):
        return [self.open_image()]

    @property
    def is_illust(self):
        return True
