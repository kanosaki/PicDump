
# config.py -- Configuration loader
from picdump import config_default


class ConfigLoader:
    def __init__(self, configfile):
        self.configfile = configfile

    def load(self):
        locs = {}
        globs = self.prepare_globals()
        exec(self.configfile, globs, locs)
        return Config(locs)

    def prepare_globals(self):
        from picdump.scheduler import Updater
        from picdump.folder import Folder
        dic = {
            'Updater': Updater,
            'Folder': Folder
        }
        dic.update(self.configfacades())
        return dic

    def configfacades(self):
        import picdump.pixiv.facade
        return {
            'Pixiv': picdump.pixiv.facade.ConfigFacade
        }


def load_default():
    return Config({
        'pixiv': config_default.pixiv,
        'folders': config_default.folders
    })


class Config:
    # config_obj: dict -- defined variables in config file
    def __init__(self, config_obj):
        pass
