from datetime import datetime

from nose.tools import *

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

class TestCSVRow:
    def test_parse_line_illust(self):
        contents = list(csv.parse(SAMPLE_LINE_ILLUST, None))  # api is not used for now
        assert_equal(1, len(contents))
        illust = contents[0]
        assert_equals(illust.illust_id, 12345678)
        assert_equal(illust.author_id, 1234567)
        assert_equal(illust.extension, 'jpg')
        assert_equal(illust.comments, 982)
        assert_equal(illust.points, 9770)
        assert_equal(illust.views, 13361)
        assert_equal(illust.caption, 'Caption String')
        assert_equals(illust.author_name, 'username')
        assert_list_equal(illust.tags, ['hoge', 'fuga', '>foo'])
        assert_list_equal(illust.tools, ['Photoshop', 'SAI'])
        assert_equal(datetime(2013, 9, 9, 17, 00, 43), illust.timestamp)
        # Illust specific
        assert_equal(illust.pages, None)
        assert_equal(illust.image_url, 'http://i1.pixiv.net/img35/img/username/12345678.jpg')

    def test_parse_line_illust(self):
        contents = list(csv.parse(SAMPLE_LINE_MANGA, None))  # api is not used for now
        assert_equal(1, len(contents))
        illust = contents[0]
        assert_equals(illust.illust_id, 12345678)
        assert_equal(illust.author_id, 1234567)
        assert_equal(illust.extension, 'png')
        assert_equal(illust.comments, 982)
        assert_equal(illust.points, 9770)
        assert_equal(illust.views, 13361)
        assert_equal(illust.caption, 'Caption String')
        assert_equals(illust.author_name, 'username')
        assert_list_equal(illust.tags, ['hoge', 'fuga', '>foo'])
        assert_list_equal(illust.tools, ['Photoshop', 'SAI'])
        assert_equal(datetime(2013, 9, 9, 17, 00, 43), illust.timestamp)
        # Manga specific
        assert_equal(illust.pages, 2)
        assert_list_equal(illust.page_urls, [
            'http://i1.pixiv.net/img35/img/username/12345678_p0.png',
            'http://i1.pixiv.net/img35/img/username/12345678_p1.png'
        ])
