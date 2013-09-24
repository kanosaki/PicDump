

import queue


class RowParser:
    def __init__(self):
        pass


class TableAPI:
    """Wraps table like apis"""
    def __init__(self, parser=None):
        self.parser = parser or RowParser()
        self.queue = queue.Queue()
        self.next_page = 1

    def __next__(self):
        pass

    def __iter__(self):
        return self

    def fetch(self, page_num):
        pass

    def fetch_next(self):
        self.fetch(self.next_page)
        self.next_page += 1

    def prefetch(self, count):
        if len(self.queue) < count:
            self.fetch_next()
            self.prefetch(count)

    @property
    def page_size(self):
        return 50

    def __len__(self):
        return len(self.queue)
