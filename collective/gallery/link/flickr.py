import flickrapi

from collective.gallery import interfaces
from collective.gallery import cache
from collective.gallery.link import BaseResource
from plone.memoize import ram
from zope import interface

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

class Link(BaseResource):
    """Flickr implementation of IGallery over Link content type"""

    def __init__(self, context):
        super(Link, self).__init__(context)
        self._flickr = None
        self._metadata = {'creator':'', 'albumName':''}
        self._user_info = {}
        self.validator = check

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


    def photos(self):
        """it depends on metdatas extracted from the url
        but we have different case:

        http://www.flickr.com/photos/rbpdesigner
        We have the username, return all photos

        http://www.flickr.com/photos/autowitch/sets/107460/

        """

        if not self.validate(): return super(Link, self).photos()

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

        if not self.validate(): return super(Link, self).creator

        return self.user_info['username']

    @property
    def title(self):
        """Return the title of the album. If you want to use link title you can
        do it in the tempalte"""

        #TODO: implement title
        return super(Link, self).title


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
        self.id = photo.get('id')
        self.thumb_url = thumb_url
        self.title = photo.get('title')
        self.description = ''
