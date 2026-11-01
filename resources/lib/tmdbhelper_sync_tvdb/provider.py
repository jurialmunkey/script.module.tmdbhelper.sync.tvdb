from jurialmunkey.ftools import cached_property
from tmdbhelper.lib.sync.providers.base import SyncProvider
from tmdbhelper_sync_tvdb.directories.item import TVDbDirectoryItem
from tmdbhelper_sync_tvdb.directories.routes import LIST_ROUTES
from tmdbhelper_sync_tvdb.settings import TVDbSettings


class Provider(SyncProvider):
    interface_version = 3
    provider_id = 'tvdb'
    display_name = 'TVDb'
    directory_item_class = TVDbDirectoryItem
    list_routes = LIST_ROUTES

    @cached_property
    def api(self):
        return self.get_api()

    def get_api(self):
        from tmdbhelper_sync_tvdb.api import TVDb
        return TVDb()

    def migrate_settings(self):
        TVDbSettings().migrate_settings()

    def is_authorized(self):
        return bool(TVDbSettings().api_key)
