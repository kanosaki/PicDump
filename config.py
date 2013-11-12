from datetime import timedelta

from picdump.folder import Folder, Updater
from picdump import pixiv
from picdump import log
from picdump.conduit import unique, cyclic
from picdump.webconsole import WebConsole
from picdump.pixiv.filters import filter_manga

log.init_logger()

cache_dir = "cache"

pixiv = pixiv.create(username="foobar", password="hogehoge")

default_source = filter_manga(unique(cyclic(
    pixiv.ranking(span=pixiv.span.daily),
    pixiv.ranking_log.days_ago(1),
    pixiv.ranking_log.days_ago(2))))

folders = [
    Folder(
        name="default",
        path="default",
        source=default_source,
        updater=Updater(
            interval=timedelta(seconds=5),
            clear_dir=True,
            source_reset=True,
            size=pixiv.page_size * 2
        )
    )
]

webconsole = WebConsole(
    port=4000,
    host='localhost',
    html_dir='html',
)
# pymode:lint=0
