from lxml import etree


VIDEO_PREFIX = "/video/yousee"

NAME = L('Title')

ART  = 'art-default.jpg'
ICON = 'icon-default.png'
LIVE_SOURCE_URL = "http://yousee.tv/feeds/player/livetv"

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
        #Log.Debug(node.tag)
        url = "http://yousee.tv/livetv/%s"
        name = node.xpath('./name')[0].text
        id = node.xpath('./id')[0].text
        #thumb = node.xpath('/logo_large')[0].text
        dir.add(VideoClipObject(rating_key = url % id, key = url % id, source_title = "YouSee", title = name, items = [MediaObject(parts = [PartObject(key = WebVideoURL(url % id))])]))
#        ret.append((node.xpath('./id')[0].text, node.xpath('./name')[0].text))
    
    
#    for event, element in etree.iterparse(etree.tostring(sources), events=("start", "end")):
#        Log.Debug("%5s, %4s, %s" % (event, element.tag, element.text))
#    Log.Debug(sources[0].tag)
#    channels = etree.SubElement(sources, 'channels')
#    Log.Debug(etree.tostring(channels))
##    Log.Debug(channels.tag)
#    channel = etree.SubElement(channels, 'channel')
#    Log.Debug(etree.tostring(channel))
#    Log.Debug(channel.tag)
#    Log.Debug(len(channels))
#    Log.Debug(len(channels))
#    Log.Debug(len(sources))
#    Log.Debug(len(channel))
#    for channel in channels:
#        Log.Debug(channel.tag)
    #Log.Debug(sources('channels'))
#    for child in sources:
#        Log.Debug(child.tag)
#    Log.Debug(sources('channels'))
    return dir


def CallbackExample(sender):

    return MessageContainer("Not implemented","In real life, you'll make more than one callback,\nand you'll do something useful.\nsender.itemTitle=%s" % sender.itemTitle)

  
