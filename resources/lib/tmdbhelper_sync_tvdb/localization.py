from xbmcaddon import Addon
from tmdbhelper.lib.addon.plugin import get_localized as get_core_localized


ADDON = Addon('script.module.tmdbhelper.sync.tvdb')
LOCALIZED_IDS = frozenset((32460,))


def get_localized(localize_int=0):
    if localize_int in LOCALIZED_IDS:
        return ADDON.getLocalizedString(localize_int)
    return get_core_localized(localize_int)
