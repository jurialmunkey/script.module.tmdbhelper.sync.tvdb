from jurialmunkey.ftools import cached_property
from tmdbhelper.lib.items.directories.base.basedir_item import BaseDirItem
from tmdbhelper_sync_tvdb.directories.artwork import ADDONPATH, get_icon


class TVDbDirItem(BaseDirItem):
    icon_name = 'tvdb'

    @cached_property
    def art(self):
        return self.get_art()

    def get_art(self):
        return {'icon': get_icon(self.icon_name), 'landscape': f'{ADDONPATH}/resources/fanart.jpg'}


class TVDbDirectoryItem(TVDbDirItem):
    priority = 190
    label = 'TVDb'
    params = {'info': 'tvdb_directory'}
    types = (None,)
