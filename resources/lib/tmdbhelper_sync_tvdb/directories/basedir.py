from tmdbhelper_sync_tvdb.directories.item import TVDbDirItem
from tmdbhelper_sync_tvdb.consts import TVDB_DISCLAIMER
from tmdbhelper_sync_tvdb.localization import get_localized
from jurialmunkey.ftools import cached_property


class BaseDirItemTVDbAwards(TVDbDirItem):
    priority = 100
    label_localized = 32460
    label_type = 'localize'
    params = {'info': 'tvdb_awards'}
    infolabels = {'plot': TVDB_DISCLAIMER}
    icon_name = 'awards'
    types = ('both', )

    @cached_property
    def label(self):
        return self.get_label()

    def get_label(self):
        return get_localized(self.label_localized)


class BaseDirItemTVDbGenres(TVDbDirItem):
    priority = 200
    label_localized = 135
    label_type = 'reversed'
    params = {'info': 'tvdb_genres'}
    infolabels = {'plot': TVDB_DISCLAIMER}
    icon_name = 'genres'
    types = ('both', )


def get_all_tvdb_class_instances():
    from tmdbhelper.lib.addon.module import get_all_module_class_objects_by_priority
    return [clobj() for clobj in get_all_module_class_objects_by_priority(__name__)]
