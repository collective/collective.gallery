#from picasa getting started
import gdata.photos.service
import gdata.media
import gdata.geo
import logging
import urllib
import urlparse
from urllib import urlencode

from collective.gallery import interfaces
from collective.gallery.link import DummyResource

from zope import interface
from zope import component

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
    url_splited = url.split('/')
    return starts and len(url_splited)>4

dummy = DummyResource()

class Link(object):
    """Picasa implements of IGallery over Link content type
    please check http://code.google.com/intl/fr/apis/picasaweb/docs/1.0/reference.html
    for a complete reference of kwargs
    """
    interface.implements(interfaces.IGallery)
    component.adapts(interfaces.IATLink)

    def __init__(self, context):
        self.context = context
        self.width = 400
        self.height = 400
        self.url = context.getRemoteUrl()
        self.url_parsed = urlparse.urlparse(self.url)

    def validate(self):
        return check(self.url)

    @property
    def creator(self):

        if not self.validate(): return dummy.creator

        if len(self.url_parsed)>2:
            if len(self.url_parsed[2].split('/')) > 2:
                return self.url_parsed[2].split('/')[1]

    @property
    def albumName(self):
        if len(self.url_parsed)>2:
            if len(self.url_parsed[2].split('/')) > 2:
                return self.url_parsed[2].split('/')[2]

    @property
    def authkey(self):
        if len(self.url_parsed)>3:
            if self.url_parsed[4] and '=' in self.url_parsed[4]:
                return self.url_parsed[4].split('=')[1]

    def photos(self):

        if not self.validate(): return dummy.photos()

        kwargs = {}
        kwargs['kind'] = 'photo'
        kwargs['imgmax'] = self.imgmax(self.width, self.height)

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

        if not self.validate(): return dummy.title

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

    def search(self, query):
        return []
    
    def add(self, photos):
        pass


class Photo(object):
    """Photo implementation"""
    interface.implements(interfaces.IPhoto)

    def __init__(self, photo):
        self.url = photo.content.src
        self.thumb_url = photo.media.thumbnail[0].url
        self.title = photo.title.text
        self.description = photo.summary.text or ''
        self.exif = Exif(photo)

class Exif(object):
    """Exif implementation for picasa"""
    interface.implements(interfaces.IExif)

    def __init__(self, photo):
        exif = photo.exif
        attrs = ('distance','exposure', 'flash', 'focallength', 'fstop',
                 'imageUniqueID', 'iso', 'make', 'model', 'time')
        for attr in attrs:
            if getattr(exif, attr, None):
                setattr(self, attr, getattr(exif,attr).text)
