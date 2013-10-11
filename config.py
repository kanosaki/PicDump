from datetime import timedelta
from picdump.folder import Folder, Updater
from picdump.pixiv.facade import ConfigFacade as Pixiv


pixiv = Pixiv(username="foobar", password="hogehoge")


folders = [
    Folder(
        path="default",
        source=pixiv.ranking(span=pixiv.span.daily),
        updater=Updater(
            interval=timedelta(hours=1),
            folder_clear=True,
            source_reset=True,
            size=pixiv.page_size
        )
    )
]
# pymode:lint=0
