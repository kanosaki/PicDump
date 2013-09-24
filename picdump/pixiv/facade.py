
from picdump.pixiv import api


class ConfigFacade:
    def __init__(self, username=None, password=None):
        self.api = api.API()
        self.ranking = self.api.ranking
        self.search = self.api.search
        self.page_size = 50
        self.content_type = api.RankingContentType
        self.search_mode = api.SearchMode
        self.span = api.RankingSpan
