from tmdbhelper_sync_tvdb.directories.mapper_static import TVDbStaticItemMapper
from tmdbhelper_sync_tvdb.directories.mapper_items import TVDbAwardItemMapper
from tmdbhelper.lib.items.directories.lists_default import ListDefault, ListSliceProperties
from tmdbhelper.lib.sync.providers.registry import SyncProviderRegistry
from jurialmunkey.ftools import cached_property


class ListTVDbProperties(ListSliceProperties):
    item_mapper_class = TVDbStaticItemMapper
    unconfigured_item_data = None
    sorting_key = None
    sorting_rev = False

    @cached_property
    def plugin_category(self):
        return self.get_plugin_category()

    def get_plugin_category(self):
        plugin_category = self.request.get('name') if isinstance(self.request, dict) else None
        plugin_category = plugin_category or self.plugin_name.format(localized=self.localized, plural=self.plural)
        return plugin_category

    @cached_property
    def request(self):
        return self.tvdb_api.get_request_lc(self.url, **self.request_url_kwargs)

    @cached_property
    def results(self):
        return self.request[self.results_key] if self.request and self.results_key else self.request

    def get_uncached_items(self):
        return [self.get_mapped_item(meta) for meta in (self.results or [])]

    def get_mapped_item(self, item, add_infoproperties=None):
        return self.item_mapper_class(item, add_infoproperties).item

    @cached_property
    def request_url_params(self):
        """ for formatting url path """
        return {}

    @cached_property
    def request_url_kwargs(self):
        """ additional kwargs to add to request """
        return {}

    @cached_property
    def url(self):
        return self.request_url.format(**self.request_url_params)

    @cached_property
    def sorted_items(self):
        return self.get_sorted_items()

    def get_sorted_items(self):
        sorted_items = self.filtered_items
        if self.sorting_key:
            sorted_items = sorted(sorted_items, key=self.sorting_key, reverse=self.sorting_rev)
        return sorted_items[self.item_a:self.item_z]


class ListTVDbMediaProperties(ListTVDbProperties):
    item_mapper_class = staticmethod(TVDbAwardItemMapper)
    add_infoproperties = None

    @cached_property
    def cache_name(self):
        return self.get_cache_name()

    def get_cache_name(self):
        cache_name_list = [f'{k}={v}' for k, v in self.request_url_kwargs.items()]
        cache_name_list = sorted(cache_name_list)
        cache_name_list = [self.class_name, self.tmdb_type, self.url] + cache_name_list
        return '_'.join(map(str, cache_name_list))

    def get_uncached_items(self):
        return self.results or []

    def get_mapped_item(self, item, add_infoproperties=None):
        mapped_item = self.item_mapper_class(item, add_infoproperties or self.add_infoproperties)
        if mapped_item is None:
            return
        mapped_item.tmdb_id = self.get_tmdb_id(mapped_item)
        return mapped_item.item if mapped_item.tmdb_id else None

    def get_tmdb_id(self, mapper):
        from tmdbhelper.lib.query.database.database import FindQueriesDatabase
        query_database = FindQueriesDatabase()
        params = {'tmdb_type': mapper.tmdb_type, 'query': mapper.title}
        tmdb_id = query_database.get_tmdb_id(year=mapper.year, **params)
        return tmdb_id or query_database.get_tmdb_id(**params)

    def get_mapped_items(self, sorted_items):
        from tmdbhelper.lib.addon.thread import ParallelThread
        with ParallelThread(sorted_items, self.get_mapped_item) as pt:
            mapped_items = pt.queue
        return [i for i in mapped_items if i]

    def get_sorted_items(self):
        return self.get_mapped_items(super().get_sorted_items())


class ListTVDb(ListDefault):
    list_properties_class = ListTVDbProperties

    def configure_list_properties(self, list_properties):
        list_properties = super().configure_list_properties(list_properties)
        list_properties.plugin_name = '{localized}'
        list_properties.tvdb_api = SyncProviderRegistry().get_provider('tvdb').api
        list_properties.results_key = None
        list_properties.page_length = 4
        return list_properties

    def get_items(self, tmdb_type=None, **kwargs):
        return super().get_items(tmdb_type=tmdb_type, **kwargs)
