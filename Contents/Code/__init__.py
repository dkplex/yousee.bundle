from lxml import etree


VIDEO_PREFIX = "/video/yousee"

NAME = L('Title')

ART  = 'art-default.png'
ICON = 'icon-default.png'
LIVE_SOURCE_URL = "http://yousee.tv/feeds/player/livetv/%s"

####################################################################################################

def Start():

    Plugin.AddPrefixHandler(VIDEO_PREFIX, VideoMainMenu, NAME, ICON, ART)

    Plugin.AddViewGroup("InfoList", viewMode="InfoList", mediaType="items")
    Plugin.AddViewGroup("List", viewMode="List", mediaType="items")
    
    MediaContainer.title1 = NAME
    MediaContainer.viewGroup = "List"
    MediaContainer.art = ART
    DirectoryItem.thumb = R(ICON)
    VideoItem.thumb = R(ICON)
    HTTP.Headers['User-Agent'] = "Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10.6; en-US; rv:1.9.2.13) Gecko/20101203 Firefox/3.6.13"

    HTTP.CacheTime = CACHE_1HOUR
def VideoMainMenu():

    dir = ObjectContainer(view_group = "List", title1 = NAME, title2 = "Live TV", art = R(ART))
    sources = XML.ElementFromURL(LIVE_SOURCE_URL %'')

    
    for node in sources.xpath('//channel'):
        url = "http://yousee.tv/livetv/%s"
        name = node.xpath('./name')[0].text
        id = node.xpath('./id')[0].text
        thumb = node.xpath('./logo_large')[0].text
        metadataXML = XML.ElementFromURL(LIVE_SOURCE_URL % String.Quote(id) )
        metadataParent = metadataXML.xpath('.//programs')[0].xpath('./program')
        summary = ""
        for metadata in metadataParent:         
            starttime = str(metadata.xpath('./start')[0].text).split('T',1)[1].rsplit(':',2)[0]
            stoptime = str(metadata.xpath('./end')[0].text).split('T',1)[1].rsplit(':',2)[0]
            metatitle = str(metadata.xpath('./title')[0].text) + '\n'
            metasummary = metadata.xpath('./description')[0].text
            if metasummary is None:
                metasummary = ""
            else:
                metasummary = str(metasummary) + '\n'
            summary += metatitle +  '(' + starttime + ' - ' + stoptime + ')\n' +metasummary +'\n'
        dir.add(VideoClipObject(url = url % id, title = name, thumb = thumb, summary = summary))
    return dir

