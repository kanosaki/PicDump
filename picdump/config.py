
# config.py -- Configuration loader


class ConfigLoader:
    def __init__(self, configfile):
        self.configfile = configfile

    def load(self):
        locs = {}
        exec(self.configfile, {}, locs)
        return Config(locs)


class ConfigFileError(RuntimeError):
    pass


class Config:
    ATTRIBUTES = ['folders', 'cache_dir']

    # config_obj: dict -- defined variables in config file
    def __init__(self, config_obj):
        self._init(config_obj)
        self._config_obj = config_obj

    def _init(self, obj):
        missing_attributes = []
        for attr in self.ATTRIBUTES:
            if attr in obj:
                setattr(self, attr, obj[attr])
            else:
                missing_attributes.append(attr)
        if missing_attributes:  # if there are missing attributes
            missing_attrs = ', '.join(missing_attributes)
            raise ConfigFileError('Missing attribute(s): {}'.format(missing_attrs))
