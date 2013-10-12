from datetime import timedelta
from picdump.folder import Folder, Updater
from picdump import pixiv


pixiv = pixiv.create(username="foobar", password="hogehoge")


folders = [
    Folder(
        path="default",
        source=pixiv.ranking(span=pixiv.span.daily),
        updater=Updater(
            interval=timedelta(hours=3),
            clear_dir=True,
            source_reset=True,
            size=pixiv.page_size
        )
    )
]
# pymode:lint=0
