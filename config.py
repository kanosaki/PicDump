from datetime import timedelta

from picdump.folder import Folder, Updater
from picdump import pixiv
from picdump import log

log.init_logger()

cache_dir = "cache"

pixiv = pixiv.create(username="foobar", password="hogehoge")

folders = [
    Folder(
        name="default",
        path="default",
        source=pixiv.ranking(span=pixiv.span.daily),
        updater=Updater(
            interval=timedelta(seconds=5),
            clear_dir=True,
            source_reset=True,
            size=pixiv.page_size
        )
    )
]
# pymode:lint=0
