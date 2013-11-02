
from nose.tools import *

from picdump.pixiv.api import API, RankingSpan, RankingContentType


class DummyAdapter:
    def __init__(self, return_value):
        self.return_value = return_value
        self.called = False

    def get_text(self, url):
        if self.called:
            return ""
        else:
            self.called = True
            return self.return_value

SAMPLE_LINE = '"12345678","1234567","jpg","Title","35","2Q",' + \
    '"http://i1.pixiv.net/img35/img/username/mobile/' + \
    '12345678_128x128.jpg",,,' + \
    '"http://i1.pixiv.net/img35/img/username/mobile/12345678_480mw.jpg"' + \
    ',,,"2013-09-09 17:00:43","進撃の巨人 リヴァイ ペトラ・ラル' + \
    'リヴァペト クリック推奨 涙腺崩壊 なにこれ泣いた ' + \
    '進撃の巨人1000users入り","Photoshop SAI","982","9770",' + \
    '"13361","Caption String",,,,"2242","0","username",,' + \
    '"0",,,"http://i1.pixiv.net/img35/profile/username/mobile/1234567_80.jpg",'


class TestAPI:
    def test_ranking(self):
        dummy_adapter = DummyAdapter(SAMPLE_LINE)
        api = API(dummy_adapter)
        result = api.ranking(RankingSpan.daily, RankingContentType.rookie)
        result = list(result)
        assert_equal(1, len(result))
