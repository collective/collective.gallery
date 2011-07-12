#from picasa getting started
import gdata.photos.service
import gdata.media
import gdata.geo
import logging
import urlparse
from urllib import urlencode

from zope import interface

from collective.gallery import interfaces
from collective.gallery.link import BaseResource

logger = logging.getLogger('collective.gallery')

SIZES = (32, 48, 64, 72, 104, 144, 150, 160, 94, 110, 128, 200, 220, 288, 320,
          400, 512, 576, 640, 720, 800, 912, 1024, 1152, 1280, 1440, 1600)


def check(url):
    """Ex:

    >>> check('http://picasaweb.google.fr/ceronjeanpierre/PhotosTriEsDuMariage#')
    True
    >>> check('http://picasaweb.google.com')
    False
    """
    starts = url.startswith("http://picasaweb.google")
    starts_https = url.startswith("https://picasaweb.google")
    url_splited = url.split('/')
    return (starts or starts_https) and len(url_splited)>4

class Link(BaseResource):
    """Picasa implements of IGallery over Link content type
    please check http://code.google.com/intl/fr/apis/picasaweb/docs/1.0/reference.html
    for a complete reference of kwargs
    """

    def __init__(self, context):
        super(Link, self).__init__(context)
        self.url_parsed = urlparse.urlparse(self.url)
        query = {}
        for q_string in self.url_parsed.query.split('&'):
            q_splited = q_string.split('=')
            if len(q_splited)>1:
                key = q_splited[0]
                value = q_splited[1]
                query[key] = value
        self.query = query
        self.validator = check

    @property
    def creator(self):

        if not self.validate(): return super(Link, self).creator

        path = self.url_parsed.path.split('/')
        if len(path)>1:
            return path[1]

    @property
    def albumName(self):
        path = self.url_parsed.path.split('/')
        if len(path)>2:
            return path[2]

    @property
    def authkey(self):
        if 'authkey' in self.query:
            return self.query['authkey']

    def photos(self):

        if not self.validate(): return super(Link, self).photos()

        kwargs = {}
        kwargs['kind'] = 'photo'
        kwargs['imgmax'] = self.imgmax(self.width, self.height)
        kwargs['thumbsize'] = '72c'

        authkey = self.authkey
        if authkey:
            kwargs['authkey'] = authkey

        url = '/data/feed/api/user/%s/album/%s?'%(self.creator, self.albumName)
        url += urlencode(kwargs)

        photos = self._gdata_photos(url)
        results = self._build_structure(photos)
        return results

    def imgmax(self, width=None, height=None):
        """Check Picasa Web Albums query parameters reference"""
        imgmax = 0
        if width is None:
            imgmax = self.height
        elif height is None:
            imgmax = self.width
        else:
            imgmax = min(width, height)
        while imgmax not in SIZES and imgmax > 0:
            imgmax = imgmax -1
        return imgmax

    def _build_structure(self, photos):
        results = []

        for photo in photos:
            results.append(Photo(photo))

        return results

    @property
    def title(self):
        """Return the title of the album. If you want to use link title you can
        do it in the tempalte"""

        if not self.validate(): return super(Link, self).title

        url = '/data/feed/api/user/%s/album/%s'%(self.creator, self.albumName)
        if self.authkey:
            url += '?' + urlencode({'authkey':self.authkey})
        title = self._album_title(url)
        return title

    def _gdata_title(self, url):
        gd_client = gdata.photos.service.PhotosService()
        try:
            album = gd_client.Get(url)
            return album.title.text.decode('utf-8')
        except:
            logger.info('PICASAWEB URL DOESN T WORK: %s %s'%(self.context, url))
            return u""

    def _gdata_photos(self, url):

        gd_client = gdata.photos.service.PhotosService()

        try:
            photos = gd_client.GetFeed(url)
            return photos.entry
        except Exception, e:
            msg = 'PICASAWEB URL Exception: %s %s. Exception: %s'
            logger.info(msg%(self.context, url, e))
            return []

class Photo(object):
    """Photo implementation specific to picasaweb service"""
    interface.implements(interfaces.IPhoto)

    def __init__(self, photo):
        self.id = photo.gphoto_id.text
        self.url = photo.content.src
        self.thumb_url = photo.media.thumbnail[0].url
        self.title = photo.title.text
        self.description = photo.summary.text or ''
