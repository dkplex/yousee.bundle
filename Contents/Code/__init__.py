from lxml import etree


VIDEO_PREFIX = "/video/yousee"

NAME = L('Title')

ART  = 'art-default.jpg'
ICON = 'icon-default.png'
LIVE_SOURCE_URL = "http://yousee.tv/feeds/player/livetv/"

####################################################################################################

def Start():

    Plugin.AddPrefixHandler(VIDEO_PREFIX, VideoMainMenu, NAME, ICON, ART)

    Plugin.AddViewGroup("InfoList", viewMode="InfoList", mediaType="items")
    Plugin.AddViewGroup("List", viewMode="List", mediaType="items")
    
    MediaContainer.title1 = NAME
    MediaContainer.viewGroup = "List"
    MediaContainer.art = R(ART)
    DirectoryItem.thumb = R(ICON)
    VideoItem.thumb = R(ICON)
    HTTP.Headers['User-Agent'] = "Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10.6; en-US; rv:1.9.2.13) Gecko/20101203 Firefox/3.6.13"
    HTTP.CacheTime = CACHE_1HOUR
def VideoMainMenu():

    dir = ObjectContainer(view_group = "List", title1 = NAME, title2 = "Live TV", art = R(ART))
    sources = XML.ElementFromURL(LIVE_SOURCE_URL)
    ret = []
    for node in sources.xpath('//channel'):
        url = "http://yousee.tv/livetv/%s"
        name = node.xpath('./name')[0].text
        id = node.xpath('./id')[0].text
        Log.Debug(url % id)
        dir.add(VideoClipObject(url = url % id, title = name))
    return dir
