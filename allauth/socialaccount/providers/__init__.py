from django.conf import settings

from allauth.compat import importlib


class ProviderRegistry(object):
    def __init__(self):
        self.provider_map = {}
        self.loaded = False

    def get_list(self):
        self.load()
        return self.provider_map.values()

    def register(self, cls):
        self.provider_map[cls.id] = cls()

    def by_id(self, id):
        self.load()
        return self.provider_map[id]

    def as_choices(self):
        self.load()
        for provider in self.get_list():
            yield (provider.id, provider.name)

    def load(self):
        # TODO: Providers register with the provider registry when
        # loaded. Here, we build the URLs for all registered providers. So, we
        # really need to be sure all providers did register, which is why we're
        # forcefully importing the `provider` modules here. The overall
        # mechanism is way to magical and depends on the import order et al, so
        # all of this really needs to be revisited.
        if not self.loaded:
            for app in settings.INSTALLED_APPS:
                provider_module = app + '.provider'
                try:
                    importlib.import_module(provider_module)
                except ImportError:
                    pass
            self.loaded = True

registry = ProviderRegistry()
