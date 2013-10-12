import datetime
import itertools
from picdump import scheduler


DEFAULT_UPDATE_INTERVAL = datetime.timedelta(hours=1)


class Folder:
    def __init__(self, path=None, source=None, updater=None):
        if path is None:
            raise Exception("path required")
        if source is None:
            raise Exception("source for {} is required".format(path))
        if updater is None:
            raise Exception("update for {} is required".format(path))
        self.path = path
        self.source = source
        self.updater = updater

    def start_dump(self):
        raise NotImplementedError()

    def clear(self):
        raise NotImplementedError()

    def sink(self, it):
        raise NotImplementedError()


class Updater(scheduler.Worker):
    def __init__(self,
                 interval=DEFAULT_UPDATE_INTERVAL,
                 clear_dir=True,
                 source_reset=True,
                 size=50):
        super().__init__(interval)
        self.folder_clear = clear_dir
        self.source_reset = source_reset
        self.size = size
        self.target_folder = None

    def start(self, folder):
        self.target_folder = folder
        super().start()

    def work(self):
        folder = self.target_folder
        if self.folder_clear:
            folder.clear()
        if self.source_reset:
            folder.source.reset()
        contents = itertools.islice(folder.source, self.size)
        folder.sink(contents)






