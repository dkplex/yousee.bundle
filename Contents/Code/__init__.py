#import yousee

VIDEO_PREFIX = "/video/yousee"
#MUISC_PREFIX = "/music/yousee"


NAME = L('Title')

ART  = 'art-default.png'
ICON = 'icon-default.png'
LIVE_SOURCE_URL = "http://yousee.tv/feeds/player/livetv/%s"
APPKEY = 'Plex'
APIKEY = 'qUkcfVVjosq3910c6LSN6pBg0O2XTyjz8kiwUc3L'
APIURL = 'http://api.yousee.tv/rest/'


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
#    HTTP.Headers['User-Agent'] = "Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10.6; en-US; rv:1.9.2.13) Gecko/20101203 Firefox/3.6.13"
    HTTP.Headers['X-API-KEY'] = APIKEY

    HTTP.CacheTime = CACHE_1HOUR
def ValidatePrefs():
	if Prefs['usr'] and Prefs['pwd']:
		try:
			usr = Users().user()
			Log.Debug(usr.errors)
			
		except:
			Log.Debug('Error')
		
def VideoMainMenu():
    dir = ObjectContainer(view_group = "List", title1 = NAME, title2 = "Live TV", art = R(ART))
    for channel in Livetv().allowed_channels():

     	#thumb = channel['logos'].get('mega', channel['logos'].get('super', channel['logos'].get('extralarge', channel['logos'].get('large', channel['logos'].get('small, R(ICON')))))
     	thumb = channel['logos'].get('mega') if channel['logos'].get('mega') != "" else channel['logos'].get('super') if channel['logos'].get('super') != ""else channel['logos'].get('extralarge') if channel['logos'].get('extralarge') != "" else channel['logos'].get('large') if channel['logos'].get('large') != "" else channel['logos'].get('small') if channel['logos'] != "" else R(ICON)

    	Log.Debug(thumb)
    	dir.add(VideoClipObject(url = 'http://yousee.tv/livetv/%s' % channel.get('shortname'), title = channel.get('nicename'), thumb = thumb))
	
#	dir.add(PrefsObject(title = 'Indstillinger', thumb = R(ICON) ))
    	
    return dir

#===============================================================================
#   
# JSON Calls for Yousee   
#===============================================================================

class Livetv:
	def __init__(self):
		pass
	# Returns metadata for channel based on channel id.
	def channel(self, id):
		return JSON.ObjectFromURL(APIURL + 'livetv/channel/id/%s/json' % id)
	# Returns channels sorted by most popular. 
	# Based on data from yousee.tv
	def popularchannels(self):
		return JSON.ObjectFromURL(APIURL + 'livetv/popularchannels/json')
	# Returns channels available for streaming from requesting ip address
	def allowed_channels(self, clientip = Network.PublicAddress, branch = 'yousee', apiversion = 2):
		return JSON.ObjectFromURL( APIURL + 'livetv/allowed_channels/branch/%s/clientip/%s/apiversion/%s/json' % (branch, clientip, apiversion))
	#Returns list of channels that should be presented to the user. NOTE: this is not the list of allowed channels.
	#A non-yousee broadband user will get a list of channels
	#from “Grundpakken”.
	def suggested_channels(self):
		return JSON.ObjectFromURL(APIURL + 'livetv/suggested_channels/json')
	#Returns absolute streaming URL for channel. Channel rights are based on client ip address.
	def streamurl(self, channel_id, terminal, drmclientid, session_id, client = 'http', application = 'Plex'):
		return JSON.ObjectFromURL(APIURL + 'livetv/streamurl/channel_id/%s/client/%s/application/%s/erminal/%s/drmclientid/%s/json' % (channel_id, client, application, terminal, drmclientid), headers = {'X-Yspro':session_id})
class Movie:
	# Returns meta data for one movie
	def movieinfo(self, id,apiversion=2):
		return JSON.ObjectFromURL(APIURL + 'movie/movieinfo/id/%s/apiversion/2/json' % id)
	# Returns all available themes
	def themes(self, include100movies = 0, only100movies = 0, onlysvod = 0):
		return JSON.ObjectFromURL(APIURL + 'movie/themes/include100movies/%s/only100movies/%s/onlysvod/%s/json' % (include100movies, only100movies, onlysvod))
	# Returns all available genres
	def genres(self, include100movies = 0, only100movies = 0,onlysvod = 0):
		return JSON.ObjectFromURL(APIURL + 'movie/genres/include100movies/%s/only100movies/%s/onlysvod/%s/json' % (include100movies, only100movies, onlysvod))
	# Returns all available movies
	def all(self, sort = 'title', sortdirection = 'asc', offset = 0, limit = -1, include100movies = 0, excludetvseries = 0, onlysvod = 0, only100movies = 0, onlytvseries = 0, year = 0):
		return JSON.ObjectFromURL(APIURL + 'movie/all/sort/%s/sortdirection/%s/offset/%s/limit/%s/include100movies/%s/excludetvseries/%s/onlysvod/%s/only100movies/%s/onlytvseries/%s/year/%s/json' % (sort, sortdirection, limit, include100movies, excludetvseries, onlysvod, only100movies, onlytvseries, year))
	# Returns movies, moviepackages and tv show seasons based on search query
	def search(self, query, offset = 0, limit = -1, include100movies = 0, excludetvseries = 0, onlysvod = 0, only100movies = 0, onlytvseries = 0, apiversion = 2, year = 0):
		return JSON.ObjectFromURL(APIURL + 'movie/search/query/%s/offest/%s/include100movies/%s/excludetvseries/%s/onlysvod/%s/only100movies/%s/onlytvseries/%s/apiversion/%s/year/%s/json' % (query, offset, limit, include100movies, excludetvseries, onlysvod, only100movies, onlytvseries, apiversion, year))
	# Returns typeahead search terms
	def typeahead_search(self, query, include100movies = 0, excludetvseries = 0, onlysvod = 0, only100movies = 0, onlytvseries = 0, year = 0):
		return JSON.ObjectFromURL(APIURL + 'movie/typeahead_search/query/%s/include100movies/%s/excludetvseries/%s/onlysvod/%s/only100movies/%s/onlytvseries/%s/year/%s/json' % (query , include100movies, excludetvseries, onlysvod, only100movies, onlytvseries, year)) 
	# Returns all movies in genre
	def in_genre(self, genre, sort = 'title', sortdirection = 'asc', offset = 0, limit = -1, include100movies = 0, excludetvseries = 0, onlysvod = 0, only100movies = 0, onlytvseries = 0, year = 0):
		return JSON.ObjectFromURL(APIURL + 'movie/in_genre/genre/%s/sort/%s/sortdirection/%s/offset/%s/limit/%s/include100movies/%s/excludetvseries/%s/onlysvod/%s/only100movies/%s/onlytvseries/%s/year/%s/json' % (genre, sort, sortdirection, offset, limit, include100movies, excludetvseries,  onlysvod, only100movies, onlytvseries, year))
	# Returns all movies in theme
	def in_theme(self, theme, sort = 'title', sortdirection = 'asc', offset = 0, limit = -1, include100movies = 0, excludetvseries = 0, onlysvod = 0, only100movies = 0, onlytvseries = 0, year = 0):
		return JSON.ObjectFromURL(APIURL + 'movie/in_theme/theme/%s/sort/%s/sortdirection/%s/offset/%s/limit/%s/include100movies/%s/excludetvseries/%s/onlysvod/%s/only100movies/%s/onlytvseries/%s/year/%s/json' % (theme, sort, sortdirection, offset, limit, include100movies, excludetvseries, onlysvod, only100movies, onlytvseries, year))
	#Returns related movies for movie.
	#Data is based on matching genres orders by popularity
	def related(self, id, only100movies = 0, onlysvod = 0, onlytvseries = 0):
		return JSON.ObjectFromURL(APIURL + 'movies/related/id/%s/only100movies/%s/onlysvod/%s/onlytvseries/%s/json' % (id, only100movies, onlysvod, onlytvseries))
	#Returns accepted payment methods for movie renting
	def supported_payment_methods(self, amount):
		return JSON.ObjectFromURL(APIURL + 'movies/supported_payment_methods/amount/%s/json' % amount)
	#Creates order in yousee.tv backend. This is first step in the two-step procedure for generating orders
	def order(self, yspro, id, reference_id, client_ip = Network.PublicAddress, ytype = 'movie'):
		return JSON.ObjectFromURL(APIURL + 'movies/order/id/%s/reference_id/%s/client_ip/%s/type/%s/json' % (id, reference_id, client_ip, ytype), headers = {'X-Yspro':yspro})
	#Confirms order in yousee.tv backend. This is the second step in the two-step procedure for generating orders.
	#A receipt is sent to the customer upon successful confirmation of order
	def order_confirm(self, yspro, order_id, transaction_id, pincode, giftcode, trust, fee):
		url = 'movies/order_confirm/order_id/%s/' % (order_id, transaction_id)
		if pincode: 
			url += 'pincode/%s/' % pincode
			trust = True
		if giftcode:
			url += 'giftcode/%s/' % giftcode
			trust = True
		if trust:
			url += 'trust/true/'
		url += 'fee/%s/json' % fee
		return JSON.ObjectFromURL(APIURL + url, headers = {'X-Yspro':yspro})
	# Returns information needed for embedding player.
	def playerdata(self, yspro, id):
		return JSON.ObjectFromURL(APIURL + 'movies/playerdata/id/%s/json' % id, headers = {'X-Yspro':yspro})
	# Returns HLS streaming URL
	def streamurl(self, session_id, id, drmclientid, application = 'Plex', terminal = 'Plex_9'):
		return JSON.ObjectFromURL(APIURL + 'movies/streamurl/id/%s/application/%s/terminal/%s/drmclientid/%s/json' % (id, application,terminal,drmclientid), headers = {'X-Yspro':session_id})
	# Returns all or subset of moviepackages
	def moviepackages(self, sort = 'name', sortorder = 'asc', offset = 0, limit = -1):
		return JSON.ObjectFromURL(APIURL + 'movie/moviepackages/sort/%s/sortorder/%s/offset/%s/limit/%s/json' % (sort, sortorder, offset, limit))
	# Returns a single moviepackage
	def moviepackage(self, id):
		return JSON.ObjectFromURL(APIURL + 'movie/moviepackage/id/%s/json' % id)
	# Returns all or subset of tvshows
	def tvshows(self, offset = 0, limit = -1, only100movies = 0, onlysvod = 0):
		return JSON.ObjectFromURL(APIURL + 'movie/tvshows/offset/%s/limit/%s/only100movies/%s/onlysvod/%s/json' % (offset, limit, only100movies, onlysvod))
	# Returns a single tv show
	def tvshow(self, id, only100movies = 0, onlysvod = 0):
		return JSON.ObjectFromURL(APIURL + 'movie/tvshow/id/%s/only100movies/%s/onlysvod/%s/json' % (id, only100movies, onlysvod))
	# Returns a single tv show season
	def tvshowseason(self, id, only100movies=0, onlysvod =0):
		return JSON.ObjectFromURL(APIURL + 'movie/tvshowseason/id/%s/only100movies/%s/onlysvod/%s/json' % (id,only100movies,onlysvod))
class Play:
	# Returns meta data for one album
	def album(id):
		return JSON.ObjectFromURL(self, APIURL + 'play/album/id/%s/json' % id)
	# Returns meta data for one track
	def track(id):
		return JSON.ObjectFromURL(self, APIURL + 'play/track/id/%s/json' % id)
	# Returns meta data for one artist
	def artist(id):
		return JSON.ObjectFromURL(self, APIURL + 'play/artist/id/%s/json' % id)
	# Returns discography
	def artist_discography(self, id, offset = 0, limit = 5):
		if limit >50: limit = 50
		return JSON.ObjectFromURL(self, APIURL + 'play/artist_discography/id/%s/json' % id)
	# Returns playlist metadata and tracks
	def playlist(self, hash):
		return JSON.ObjectFromURL(self, APIURL + 'play/playlist/id/%s/json' % id)
	# Returns editorial list
	def list(self, ylist):
		return JSON.ObjectFromURL(self, APIURL + 'play/list/json')
class Tvguide:
	# Returns all available channels in TV guide, sorted by categories
	def channels(self):
		return JSON.ObjectFromURL(APIURL + 'tvguide/channels/json')
	# Returns all categories
	def categories(self):
		return JSON.ObjectFromURL(APIURL + 'tvguide/categories/json')
	# Returns programs
	def programs(self):
		return JSON.ObjectFromURL(APIURL + 'tvguide/programs/json')
	# Returns programs matching query
	def search(self, query):
		return JSON.ObjectFromURL(APIURL + 'tvguide/search/query/%s/json' % query)
	# Returns a list of recommended programs
	def recommendedprograms(self):
		return JSON.ObjectFromURL(APIURL + 'tvguide/recommendedprograms/json')
class Archive:
	#Returns a list of genres
	def genres(self):
		return JSON.ObjectFromURL(APIURL + 'archive/genres/json')
	# Returns a list of programs in archive
	def programs(self):
		return JSON.ObjectFromURL(APIURL + 'archive/programs/json')
	# Returns a list of allowed archive channels
	def allowed_channels(self):
		return JSON.ObjectFromURL(APIURL + 'archive/allowed_channels/json')
	# Returns a list of programs in archive matching search query
	def search(self, query):
		return JSON.ObjectFromURL(APIURL + 'archive/search/query/%s/json' % query)
	# Returns absolute streaming url for content
	def streamurl(self, id):
		return JSON.ObjectFromURL(APIURL + 'archive/streamurl/id/%s/json' % id)

class Users:
	# Logs in user and returns YS Pro session information
	def login(self, username, password):
		return JSON.ObjectFromURL(APIURL+  'users/login/username/%s/password/%s/json' % (username, password))
	# Logs out user of YSPro
	def logout(sel):
		return JSON.ObjectFromURL(APIURL + 'users/logout/json')
	# Creates new user in YSPro backend
	def user(self):
		return JSON.ObjectFromURL(APIURL + 'users/user/json')
	# Returns transaction log for user
	def transactions(self):
		return HTTP.Request(APIURL + 'users/transactions/json')
			
	# Checks if user is using YouSee Broadband
	def isyouseeip(self):
		return JSON.ObjectFromURL(APIURL + 'users/isyouseeip/json')
	# Checks if user has access to movie
	def movieaccess(self):
		return JSON.ObjectFromURL(APIURL + 'users/movieaccess/json')
	# Refreshes usersession in YSPro backend
	def keepalive(self):
		return JSON.ObjectFromURL(APIURL + 'users/keepalive/json')
	# Returns device list
	def devices(self):
		return JSON.ObjectFromURL(APIURL + 'users/devices/json')
	# POST: Add new device to device list
	# DELETE: Remove device from list
	def device(self, method = "POST"):
		return JSON.ObjectFromURL(APIURL + 'users/device/json')
	# Returns favorites
	def favorites(self):
		return JSON.ObjectFromURL(APIURL + 'users/favorites/json')
	# POST: Add new favorite
	# DELETE: Remove a favorite
	def favorite(self, method = 'POST'):
		return JSON.ObjectFromURL(APIURL + 'users/favorite/json')
	# Sorts favorites in list
	def favorites_sortorder(self):
		pass
	# POST: Saves bookmark in seconds
	# GET: Returns bookmark
	# DELETE: Removes bookmark
	def bookmark(method = 'GET'):
		pass
	# Returns all bookmarks
	def bookmarks(self):
		return JSON.ObjectFromURL(APIURL + 'users/bookmarks/json')
	# POST: Add new movie log entry
	# GET: Returns movie log
	# DELETE: Resets movielog
	def movielog(self, method = 'GET'):
		pass
	# Returns data for filmshelf
	def filmshelf(self):
		return JSON.ObjectFromURL(APIURL + 'users/filmshelf/json')

class System:
# Returns current supportmessage
	def supportmessage(self):
		return JSON.ObjectFromURL(APIURL + 'system/supportmessage/json')
	# Returns latest errormessage for device
	def errormessage(self, udid):
		return JSON.ObjectFromURL(APIURL + 'system/errormessage/udid/%s/json' % udid)

# build the rest URL
def kwargsToURL(url, **kwargs):
	
	for ysArgs in kwargs:
		url += ysArgs + '/' + kwargs[ysArgs]
	url += 'json'
	return url		