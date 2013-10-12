import unittest
from datetime import datetime

from picdump.pixiv import csv


SAMPLE_LINE_ILLUST = '"12345678","1234567","jpg","Title","35","2Q",' + \
                     '"http://i1.pixiv.net/img35/img/username/mobile/' + \
                     '12345678_128x128.jpg",,,' + \
                     '"http://i1.pixiv.net/img35/img/username/mobile/12345678_480mw.jpg"' + \
                     ',,,"2013-09-09 17:00:43","hoge fuga &gt;foo","Photoshop SAI","982","9770",' + \
                     '"13361","Caption String",,,,"2242","0","username",,' + \
                     '"0",,,"http://i1.pixiv.net/img35/profile/username/mobile/1234567_80.jpg",'

SAMPLE_LINE_MANGA = '"12345678","1234567","png","Title","35","2Q",' + \
                    '"http://i1.pixiv.net/img35/img/username/mobile/' + \
                    '12345678_128x128.jpg",,,' + \
                    '"http://i1.pixiv.net/img35/img/username/mobile/12345678_480mw.jpg"' + \
                    ',,,"2013-09-09 17:00:43","hoge fuga &gt;foo","Photoshop SAI","982","9770",' + \
                    '"13361","Caption String","2",,,"2242","0","username",,' + \
                    '"0",,,"http://i1.pixiv.net/img35/profile/username/mobile/1234567_80.jpg",'

class TestCSVRow(unittest.TestCase):
    def test_parse_line_illust(self):
        contents = list(csv.parse(SAMPLE_LINE_ILLUST, None))  # api is not used for now
        self.assertEqual(1, len(contents))
        illust = contents[0]
        self.assertEquals(illust.illust_id, 12345678)
        self.assertEqual(illust.author_id, 1234567)
        self.assertEqual(illust.extension, 'jpg')
        self.assertEqual(illust.comments, 982)
        self.assertEqual(illust.points, 9770)
        self.assertEqual(illust.views, 13361)
        self.assertEqual(illust.caption, 'Caption String')
        self.assertEquals(illust.author_name, 'username')
        self.assertListEqual(illust.tags, ['hoge', 'fuga', '>foo'])
        self.assertListEqual(illust.tools, ['Photoshop', 'SAI'])
        self.assertEqual(datetime(2013, 9, 9, 17, 00, 43), illust.timestamp)
        # Illust specific
        self.assertEqual(illust.pages, None)
        self.assertEqual(illust.image_url, 'http://i1.pixiv.net/img35/img/username/12345678.jpg')

    def test_parse_line_illust(self):
        contents = list(csv.parse(SAMPLE_LINE_MANGA, None))  # api is not used for now
        self.assertEqual(1, len(contents))
        illust = contents[0]
        self.assertEquals(illust.illust_id, 12345678)
        self.assertEqual(illust.author_id, 1234567)
        self.assertEqual(illust.extension, 'png')
        self.assertEqual(illust.comments, 982)
        self.assertEqual(illust.points, 9770)
        self.assertEqual(illust.views, 13361)
        self.assertEqual(illust.caption, 'Caption String')
        self.assertEquals(illust.author_name, 'username')
        self.assertListEqual(illust.tags, ['hoge', 'fuga', '>foo'])
        self.assertListEqual(illust.tools, ['Photoshop', 'SAI'])
        self.assertEqual(datetime(2013, 9, 9, 17, 00, 43), illust.timestamp)
        # Manga specific
        self.assertEqual(illust.pages, 2)
        self.assertListEqual(illust.page_urls, [
            'http://i1.pixiv.net/img35/img/username/12345678_p0.png',
            'http://i1.pixiv.net/img35/img/username/12345678_p1.png'
        ])
