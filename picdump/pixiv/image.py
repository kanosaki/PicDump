
from picdump import image

# Represents one image file


class Image(image.Image):
    def __init__(self, res, item):
        """
        :param res: HTTP Response from 'requests'
        :param item: picdump.pixiv.Item
        """
        res.raise_for_status()  # raise error if HTTP GET has not been correctly finished.
        self.item = item
        self.data = res.content

    @property
    def dot_and_extension(self):
        if self.item.extension:
            return '.{}'.format(self.item.extension)
        else:
            return ''

    @property
    def default_filename(self):
        item = self.item
        return '{} {}{}'.format(item.item_id, item.title, self.dot_and_extension)
