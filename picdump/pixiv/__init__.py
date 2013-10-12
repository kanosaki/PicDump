
from picdump.pixiv import facade


def create(username=None, password=None):
    return facade.Pixiv(username, password)
