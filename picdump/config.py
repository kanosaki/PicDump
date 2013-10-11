
# config.py -- Configuration loader


class ConfigLoader:
    def __init__(self, configfile):
        self.configfile = configfile

    def load(self):
        locs = {}
        exec(self.configfile, {}, locs)
        return Config(locs)


class Config:
    # config_obj: dict -- defined variables in config file
    def __init__(self, config_obj):
        self._validate_config(config_obj)
        self._config_obj = config_obj

    def _validate_config(self, obj):
        def validate():
            if 'folders' not in obj:
                yield 'Missing folders attribute'
        errors = list(validate())
        if len(errors) > 0:
            raise RuntimeError('. '.join(errors))
