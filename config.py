from datetime import timedelta


pixiv = Pixiv(username="foobar", password="hogehoge")


folders = [
    Folder(
        path="default",
        source=pixiv.ranking(span=pixiv.span.daily),
        updater=Updater(
            interval=timedelta(hours=1),
            clear_dir=True,
            reset_iteration=True,
            size=pixiv.page_size
        )
    )
]
