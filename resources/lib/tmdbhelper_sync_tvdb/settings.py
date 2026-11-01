from xbmcaddon import Addon
from jurialmunkey.window import get_property


class TVDbToken:
    token_property = 'TVDb.Token'

    @property
    def value(self):
        return get_property(self.token_property, is_type=str)

    @value.setter
    def value(self, value):
        get_property(self.token_property, set_property=str(value))


class TVDbSettings:
    addon_id = 'script.module.tmdbhelper.sync.tvdb'

    def __init__(self):
        self.addon = Addon(self.addon_id)
        self.token = TVDbToken()

    @property
    def api_key(self):
        from tmdbhelper_sync_tvdb.api_keys import API_KEY
        return self.addon.getSetting('apikey') or API_KEY

    def migrate_settings(self):
        legacy_addon = Addon('plugin.video.themoviedb.helper')
        legacy_token = get_property('tvdb_token', is_type=str) or legacy_addon.getSetting('tvdb_token')
        if not legacy_token:
            return
        destination_token = self.token.value or legacy_token
        if not self.token.value:
            self.token.value = destination_token
        if self.token.value != destination_token:
            raise RuntimeError('Unable to save migrated TVDb token')
        legacy_addon.setSetting('tvdb_token', '')
        if legacy_addon.getSetting('tvdb_token'):
            raise RuntimeError('Unable to clear legacy TVDb token')
        get_property('tvdb_token', clear_property=True)
