from xbmcaddon import Addon
from xbmcvfs import translatePath


ADDONPATH = translatePath(Addon('script.module.tmdbhelper.sync.tvdb').getAddonInfo('path'))


def get_icon(name='tvdb'):
    return f'{ADDONPATH}/resources/icons/tvdb/{name}.png'
