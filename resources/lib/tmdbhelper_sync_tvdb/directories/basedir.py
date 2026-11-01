from tmdbhelper_sync_tvdb.directories.item import TVDbDirItem
from tmdbhelper_sync_tvdb.consts import TVDB_DISCLAIMER


class BaseDirItemTVDbAwards(TVDbDirItem):
    priority = 100
    label_localized = 32460
    label_type = 'localize'
    params = {'info': 'tvdb_awards'}
    infolabels = {'plot': TVDB_DISCLAIMER}
    icon_name = 'awards'
    types = ('both', )


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
