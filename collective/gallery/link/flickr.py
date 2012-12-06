import flickrapi

from collective.gallery import interfaces
from collective.gallery import cache
from collective.gallery.link.base import BaseResource
from plone.memoize import ram
from zope import interface

API_KEY = '37f7bd2f16b0071fb536ae907473780a'

def check(url):
    return url.startswith('http://www.flickr.com')

def extract_data(url):
    """Return metadata from this flickr url
    Basicly there is 3 types of urls

        - User :
                - http://www.flickr.com/photos/princeofnorway/

        - User + sets :

            - http://www.flickr.com/photos/princeofnorway/sets/72157623726009622/

        - Tags Filters With or without Users:

            - http://www.flickr.com/photos/searchtags/1,2,3
            - http://www.flickr.com/photos/princeofnorway/searchtags/1,2,3
    """
    result = {'yahoo_account': None,
              'sets': None,
              'searchtags': None,
              'type': None,
              }
    mapping = {'photos':'yahoo_account'}
    if not check(url): return result
    url_splited = url.split('/')
    result['type'] = url_splited[3]
    if len(url_splited) > 4:
        result['yahoo_account'] = url_splited[4]
        if result['yahoo_account'] in ['searchtags', 'sets']:
            result['yahoo_account'] = None
    for m in ['photos', 'sets', 'searchtags']:
        if m in url_splited:
            try:
                val = url_splited[url_splited.index(m) + 1]
            except IndexError, e:
                val = None
            # special case: search on tags without user
            if (val in ['searchtags', 'photos', 'sets']
                and m in ['searchtags', 'photos', 'sets']):
                continue
            result[mapping.get(m, m)] = val
    return result


class Link(BaseResource):
    """Flickr implementation of IGallery over Link content type"""

    def __init__(self, context):
        super(Link, self).__init__(context)
        self._flickr = None
        self._metadata = {'creator':'', 'albumName':''}
        self._user_info = {}

    @property
    @ram.cache(cache.url_cache_key)
    def user_info(self):
        """In the url we have the yahoo account of the guy, not the username...
        """
        result = {
            'user_yahooaccount': None,
            'user_id': None,
            'username': None,
        }
        flickr = self._flickr_service()
        result['user_yahooaccount'] = extract_data(
            self.url)['yahoo_account']
        # we search on a user, because it would extracted as None otherwise
        if result['user_yahooaccount']:
            try:
                user = flickr.urls_lookupUser(url=self.url)
                result['user_id'] = user.find('user').get('id')
                result['username'] = user.find(
                    'user').find('username').text
            except Exception, e:
                # a search on photos is the only case without user
                # and we should skip the user test failure
                if not 'photos/searchtags' in self.url:
                    raise e
        return result

    def photos(self):
        """it depends on metdatas extracted from the url
        but we have different case:

        http://www.flickr.com/photos/rbpdesigner
        We have the username, return all photos

        http://www.flickr.com/photos/autowitch/sets/107460/

        """

        flickr = self._flickr_service()
        metadatas = extract_data(self.url)

        results = []
        if metadatas['type'] == 'photos':

            if metadatas['sets']:
                set = flickr.walk_set(metadatas['sets'])
                results = self._build_structure(set)
            else:
                kw = {}
                if self.user_info['user_id']:
                    kw['user_id'] = self.user_info['user_id']
                if metadatas['searchtags']:
                    kw['tags' ] = metadatas['searchtags']
                if (not 'user_id' in kw
                    and not 'tags' in kw):
                    raise Exception(
                        'invalid search, '
                        'at least user or tags is needed')
                photos = flickr.photos_search(**kw)
                results = self._build_structure(photos[0])

        return results

    def _build_structure(self, photos):
        return map(Photo, photos)

    def _flickr_service(self):
        """Return the flickr service"""
        if self._flickr: return self._flickr
        self._flickr = flickrapi.FlickrAPI(API_KEY)
        return self._flickr

    @property
    def creator(self):

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
