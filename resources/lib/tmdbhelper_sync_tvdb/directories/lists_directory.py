from jurialmunkey.ftools import cached_property
from tmdbhelper.lib.items.directories.base.lists_base import BaseDirList
from tmdbhelper.lib.items.directories.lists_default import ListDefault, ListProperties
from tmdbhelper_sync_tvdb.directories.basedir import get_all_tvdb_class_instances
from tmdbhelper_sync_tvdb.directories.mapper_directory import TVDbDirectoryItemMapper


class TVDbBaseDirList(BaseDirList):
    @property
    def basedir(self):
        return get_all_tvdb_class_instances()


class ListTVDbDirectoryProperties(ListProperties):
    plugin_name = 'TVDb'
    container_content = ''
    item_mapper_class = TVDbDirectoryItemMapper

    @cached_property
    def entries(self):
        return self.get_entries()

    def get_entries(self):
        return [
            entry for entry in TVDbBaseDirList().get_basedir()
            if not self.group or int(self.group) == entry.item.group
        ]

    @cached_property
    def type_art(self):
        return len({entry.type for entry in self.entries}) > 1

    @cached_property
    def items(self):
        return self.get_items()

    def get_items(self):
        return [self.get_mapped_item(entry) for entry in self.entries]

    def get_mapped_item(self, item, add_infoproperties=None):
        mapper = self.item_mapper_class(item, add_infoproperties)
        mapper.type_art = self.type_art
        return mapper.item


class ListTVDbDirectory(ListDefault):
    list_properties_class = ListTVDbDirectoryProperties
    kodi_details = False

    def configure_list_properties(self, list_properties):
        list_properties = super().configure_list_properties(list_properties)
        list_properties.plugin_name = 'TVDb'
        list_properties.pagination = False
        return list_properties

    def get_items(self, group=None, **kwargs):
        self.list_properties.group = group
        return self.get_items_finalised()
