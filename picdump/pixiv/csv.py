
def read(stream):
    return CSVReader(stream)


class CSVReader:
    def __init__(self, stream, rowparser=None):
        self.stream = stream

    def __next__(self):
        line = self.stream.readline()
        return self.parse_row(line)

    def parse_row(self, line):
        pass
