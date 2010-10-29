import logging
import urllib
import urlparse

from urllib import urlencode
from urllib2 import urlopen

from collective.gallery import interfaces
from collective.gallery.link import DummyResource

from zope import interface
from zope import component

#TODO: merge facebook support from garbas-fixes branch.

FACEBOOK_IMAGE_SIZES = [
    (50, 'q'),
    (180, 'a'),
    (720, 'n'), ]       # n is for original

def check(url):
    """Ex: 
    
    >>> check('http://picasaweb.google.fr/ceronjeanpierre/PhotosTriEsDuMariage#')
    True
    >>> check('http://picasaweb.google.com')
    False
    """
    starts = url.startswith('http://www.facebook.com')
    return starts

dummy = DummyResource()

class Link(object):
    """Facebook implements of IGallery over Link content type
    """
    interface.implements(interfaces.IGallery)
    component.adapts(interfaces.IATLink)

    def __init__(self, context):
        self.context = context
        self.width = 400
        self.height = 400
        self.url = context.getRemoteUrl()

    def validate(self):
        return check(self.url)

    @property
    def creator(self):
        #TODO: support this
        if not self.validate(): return dummy.creator
        return ""

    @property
    def albumName(self):
        #TODO: support this
        if not self.validate(): return dummy.creator
        return ""

    def photos(self):

        if not self.validate(): return dummy.photos()
        f = urlopen(self.url)
        html = f.read()
        f.close()
        return facebook_extract_photos(html, sizes)


    @property
    def title(self):
        #TODO: support this
        if not self.validate(): return dummy.creator
        return ""

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

#FROM GARBAS BRANCH
#        elif url.startswith('http://www.facebook.com'):
#            try:
#                f = urlopen(url)
#                html = f.read()
#                f.close()
#                return facebook_extract_images(html, sizes)
#
#            except Exception, e:
#                msg = 'FACEBOOK URL Exception: %s %s. Exception: %s'
#                logger.info(msg % (self.context, url, e))
#                return []
#
#        else:
#            return []
#
def facebook_extract_photos(html, sizes):
    start_pos = html.find('<td class="vTop hLeft">') + 23
    if start_pos == 22:
        return []
    url_start_pos = html[start_pos:].find(
        '<i style="background-image: url(') + 32 + start_pos
    url_end_pos = html[url_start_pos:].find(')') + url_start_pos
    title_start_pos = html[start_pos:].find('title="') + 7 + start_pos
    title_end_pos = html[title_start_pos:].find('"') + title_start_pos
    if url_end_pos > title_end_pos:
        end_pos = url_end_pos
    else:
        end_pos = title_end_pos

    url_thumb = html[url_start_pos:url_end_pos]
    url = url_thumb.split('.')

    def create_url(size_char):
        return '.'.join(url[:-2] + [url[-2][:-1] + size_char] + url[-1:])

    image = dict(
        title=html[title_start_pos:title_end_pos],
        description='',
        url=create_url('n'), )
    for size_name, size in sizes.items():
        image[str('url_' + size_name)] = create_url(
                get_approx_size_value(size, FACEBOOK_IMAGE_SIZES))
    return [image] + facebook_extract_images(html[end_pos:], sizes)
