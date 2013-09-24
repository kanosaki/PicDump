
class Scheduler:
    pass


class Worker:
    def next_time(self):
        pass


class Updater(Worker):
    """Folder updater"""
    def __init__(self,
                 interval=None,
                 clear_dir=False,
                 reset_iteration=False,
                 size=10):
        pass


