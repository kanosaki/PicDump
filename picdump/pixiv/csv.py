from picdump.pixiv import item
from picdump.pixiv import illust
from picdump.pixiv import manga


CSV_DELIMITER = ','
NEWLINE = '\n'


class ItemFactory:
    def __call__(self, row, api):
        if row.pages == '':
            return illust.Illust(row, api)
        else:
            return manga.Manga(row, api)


def parse(doc, api):
    item_factory = ItemFactory()
    for line in doc.split(NEWLINE):
        if line == '':
            continue
        row = CSVRow(line)
        yield item_factory(row, api)


class CSVRow:
    CELLS = {
        'illust_id': 0,
        'author_id': 1,
        'extension': 2,
        'title': 3,
        'server': 4,
        'author_screen_name': 5,
        'thumbnail': 6,
        'mobile_image': 9,
        'timestamp': 12,
        'tags': 13,
        'tools': 14,
        'comments': 15,
        'points': 16,
        'views': 17,
        'caption': 18,
        'pages': 19,
        'author_name': 24,
        'author_thumbnail': 29
    }

    def __init__(self, line, delimiter=CSV_DELIMITER):
        self.cells = [c.strip('"') for c in line.split(delimiter)]

    def __getattr__(self, key):
        if not key in self.CELLS:
            raise AttributeError()
        else:
            col = self.CELLS[key]
            return self.cells[col]

    def __getitem__(self, index):
        return self.cells[index]

    def __contains__(self, key):
        return key in self.CELLS


class CSVReader:
    def __init__(self, doc):
        self.doc = doc

    def __iter__(self):
        return self

    def __next__(self):
        line = self.stream.readline()
        if not line:  # Reaches end
            raise StopIteration()
        return self.parse_row(line)

    def on_closing(self):
        if self.close_on_finish:
            self.stream.close()

    def parse_row(self, line):
        pass



