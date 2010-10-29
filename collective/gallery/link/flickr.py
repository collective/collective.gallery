import flickrapi
from Products.CMFCore.utils import getToolByName
from urllib import urlencode

from collective.gallery import interfaces
from collective.gallery import cache
from collective.gallery.link import DummyResource
from plone.memoize import ram
from zope import interface
from zope import component

API_KEY = '37f7bd2f16b0071fb536ae907473780a'

def check(url):
    return url.startswith('http://www.flickr.com')

def extract_data(url):
    """Return metadata from this flickr url
    
    
    >>> extract_data('http://www.flickr.com/photos/princeofnorway/')
    {'yahoo_account':'princeofnorway', 'sets':None}
    >>> extranct_data('http://www.flickr.com/photos/princeofnorway/sets/72157623726009622/')
    {'yahoo_account':'princeofnorway', 'sets':'72157623726009622'}
    """
    result = {'yahoo_account':None,
              'sets':None,
              'type':None,
              }
    if not check(url): return result
    
    url_splited = url.split('/')
    result['type'] = url_splited[3]
    result['yahoo_account'] = url_splited[4]
    if len(url_splited) > 6 and url_splited[5] == 'sets':
        result['sets'] = url_splited[6]
    return result

dummy = DummyResource()

class Link(object):
    """Flickr implementation of IGallery over Link content type"""

    interface.implements(interfaces.IGallery)
    component.adapts(interfaces.IATLink)

    def __init__(self, context):
        self.context = context
        self.width = 400
        self.height = 400
        self.url = context.getRemoteUrl()
        self._flickr = None
        self._metadata = {'creator':'', 'albumName':''}
        self._user_info = {}

    @property
    @ram.cache(cache.cache_key)
    def user_info(self):
        """In the url we have the yahoo account of the guy, not the username...
        """
        flickr = self._flickr_service()
        user = flickr.urls_lookupUser(url=self.url)
        url_splited = self.url.split('/')
        result = {}
        result['user_yahooaccount'] = url_splited[4]
        result['user_id'] = user.find('user').get('id')
        result['username'] = user.find('user').find('username').text
        return result

    def validate(self):
        return check(self.url)

    def photos(self):
        """it depends on metdatas extracted from the url
        but we have different case:
        
        http://www.flickr.com/photos/rbpdesigner
        We have the username, return all photos
        
        http://www.flickr.com/photos/autowitch/sets/107460/
        
        """

        if not self.validate():
            return dummy.photos()

        flickr = self._flickr_service()
        metadatas = extract_data(self.url)
        if metadatas['type'] == 'photos':
            if metadatas['sets']:
                set = flickr.walk_set(metadatas['sets'])
                results = [Photo(photo) for photo in set]
            else:
                user_id = self.user_info['user_id']
                photos = flickr.photos_search(user_id=user_id)
                results = [Photo(photo) for photo in set]
        return results

    def _flickr_service(self):
        """Return the flickr service"""
        if self._flickr: return self._flickr
        self._flickr = flickrapi.FlickrAPI(API_KEY)
        return self._flickr

    @property
    def creator(self):

        if not self.validate(): return dummy.creator

        return self.user_info['username']

    @property
    def title(self):
        """Return the title of the album. If you want to use link title you can
        do it in the tempalte"""

        if not self.validate(): return dummy.title

        return 'title not implemented'

    def search(self, query):
        return []
    
    def add(self, photos):
        pass

class Photo(object):
    """Photo implementation"""
    interface.implements(interfaces.IPhoto)

    def __init__(self, photo):
        thumb_url = "http://farm%s.static.flickr.com/%s/%s_%s_s.jpg" % (
            photo.get('farm'), 
            photo.get('server'), 
            photo.get('id'), 
            photo.get('secret'))
        url = "http://farm%s.static.flickr.com/%s/%s_%s.jpg" % (
            photo.get('farm'), 
            photo.get('server'), 
            photo.get('id'),
            photo.get('secret'))

        self.url = url
        self.thumb_url = thumb_url
        self.title = photo.get('title')
        self.description = ''
        self.exif = None

class Exif(object):
    """Exif implementation for picasa"""
    interface.implements(interfaces.IExif)

    def __init__(self, photo):
        #TODO: get exif need a collf from service with each photo id
        attrs = ('distance','exposure', 'flash', 'focallength', 'fstop',
                 'imageUniqueID', 'iso', 'make', 'model', 'time')
        for attr in attrs:
            setattr(self, attr, "")
