import logging
import urllib
import urlparse

logger = logging.getLogger('collective.gallery.facebook')

from BeautifulSoup import BeautifulSoup
from urllib import urlencode
from urllib2 import urlopen

from collective.gallery import interfaces
from collective.gallery.link import DummyResource

from zope import interface
from zope import component

def check(url):
    """Check if the url is valid"""

    starts = url.startswith('http://www.facebook.com/album.php?')
    has_aid = 'aid=' in url
    has_id= '&id=' in url

    return starts and has_aid and has_id

dummy = DummyResource()

class Link(object):
    """Facebook implements of IGallery over Link content type
    """
    interface.implements(interfaces.IGallery)
    component.adapts(interfaces.ILink)

    def __init__(self, context):
        self.context = context
        self.width = 400
        self.height = 400
        self.url = context.getRemoteUrl()
        self.validator = check

    def validate(self):
        return self.validator(self.url)

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
        try:
            f = urlopen(self.url)
            html = f.read()
            f.close()
            soup = BeautifulSoup(html)
            anchors = soup.findAll('a', attrs={'class':'uiMediaThumb uiScrollableThumb uiMediaThumbHuge'})
            return map(Photo, anchors)

        except Exception, e:
            logger.error('FACEBOOK backend error: %s'%e)
            return dummy.photos()

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
    """Photo implementation
    http://developers.facebook.com/docs/reference/fql/photo
    """
    interface.implements(interfaces.IPhoto)

    def __init__(self, anchor):
        img = anchor.find('i')
        self.title=anchor['title']
        self.id=str(anchor['name']) #it s the facebook unique id of the photo
        style = img['style']
        link_url = str(style[len('background-image: url('):-len(');')])
        self.thumb_url = link_url.replace('_a.','_t.')
        self.url = link_url.replace('_a.','_n.')
        self.description = u''
