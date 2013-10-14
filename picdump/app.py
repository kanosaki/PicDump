import weakref

from picdump import log


class App:
    """Application root context"""
    def __init__(self, config):
        self.config = config
        inject_app(self)

    def start(self):
        for folder in self.config.folders:
            folder.start_dump()


class HasAppMixin:
    def __init__(self):
        self.__app = None
        request_injection(self)

    @property
    def app(self):
        if self.__app is None:
            raise RuntimeError('App is not initialized')
        else:
            return self.__app

    def _inject_app(self, app):
        self.__app = app
        self.on_app_injected(app)

    def on_app_injected(self, app):
        pass


class AppInjector:
    def __init__(self):
        self.targets = weakref.WeakSet()
        self.previous_injected = None
        self.allow_reinjection = False

    def inject(self, app):
        prev_app = self.previous_injected
        if prev_app is not None and prev_app != app and not self.allow_reinjection:
            raise RuntimeError('Re-injection detected')
        for target in self.targets:
            if hasattr(target, '_inject_app'):
                target.inject_app(app)
            else:
                target.app = app
        self.previous_injected = app

    def register(self, target):
        self.targets.add(target)


ROOT_INJECTOR = AppInjector()


def request_injection(target):
    ROOT_INJECTOR.register(target)


def inject_app(app):
    ROOT_INJECTOR.inject(app)

def reinject_app():
    if ROOT_INJECTOR.previous_injected is None:
        raise RuntimeError('You cannot RE-inject before injection at least once')
    ROOT_INJECTOR.inject(ROOT_INJECTOR.previous_injected)
