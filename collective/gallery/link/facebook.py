import logging

logger = logging.getLogger('collective.gallery.facebook')
try:
    from BeautifulSoup import BeautifulSoup
    HAS_DEPENDENCY = True
except ImportError:
    HAS_DEPENDENCY = False

from urllib2 import urlopen

from zope import interface

from collective.gallery import interfaces
from collective.gallery.link import BaseResource

def check(url):
    """Check if the url is valid"""

    starts = url.startswith('http://www.facebook.com/album.php?')
    has_aid = 'aid=' in url
    has_id= '&id=' in url

    return starts and has_aid and has_id


class Link(BaseResource):
    """Facebook implements of IGallery over Link content type
    """

    def __init__(self, context):
        super(Link, self).__init__(context)
        self.validator = check

    def validate(self):
        return self.validator(self.url) and HAS_DEPENDENCY

    def photos(self):

        if not self.validate(): return super(Link, self).photos()
        try:
            f = urlopen(self.url)
            html = f.read()
            f.close()
            soup = BeautifulSoup(html)
            anchors = soup.findAll('a', attrs={'class':'uiMediaThumb uiScrollableThumb uiMediaThumbHuge'})
            return map(Photo, anchors)

        except Exception, e:
            logger.error('FACEBOOK backend error: %s'%e)
            return super(Link, self).photos()

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
