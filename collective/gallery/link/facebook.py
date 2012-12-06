"""This one doesn't work any more, we need a refactor...

extract ids and play with the graph api which return json.

new facebook link: http://www.facebook.com/media/set/?set=a.416328449800.177781.275081154800&type=1
old facebook link: http://www.facebook.com/album.php?aid=177781&id=275081154800
-> https://graph.facebook.com/416328449800/photos?limit=1000

"""
import logging

logger = logging.getLogger('collective.gallery.facebook')
import json
from urllib2 import urlopen

from zope import interface

from collective.gallery import interfaces
from collective.gallery.link.base import BaseResource

def check(url):
    """Check if the url is valid"""

    old_starts = url.startswith('http://www.facebook.com/album.php?')
    has_aid = 'aid=' in url
    has_id= '&id=' in url

    starts = url.startswith('http://www.facebook.com/media/set/?set=a.')
    starts_https = url.startswith('https://www.facebook.com/media/set/?set=a.')
    dots = len(url.split('.')) == 6

    return ((starts or starts_https) and dots) or (old_starts and has_aid and has_id)


class Link(BaseResource):
    """Facebook implements of IGallery over Link content type
    """

    def __init__(self, context):
        super(Link, self).__init__(context)
        self._album_id = None
        if self.url.startswith('http://www.facebook.com/album.php?'):
            self.update_link()

    def update_link(self):
        if not self.url.startswith('http://www.facebook.com/album.php?'):
            return
        #TODO !

    def photos(self):

        album = self.album_id()
        url = "https://graph.facebook.com/%s/photos?limit=1000"%(album)
        try:
            data_str = urlopen(url).read()
            data = json.loads(data_str)
            photos = data.get('data',[])
            return self._build_structure(photos)
        except Exception, e:
            logger.error('FACEBOOK backend error: %s'%e)
        
        return []

    def album_id(self):
        if self._album_id is None:
            self._album_id = self.url.split('.')[3]
        return self._album_id

    def _build_structure(self, photos):
        return map(Photo, photos)

class Photo(object):
    """Photo implementation
    http://developers.facebook.com/docs/reference/fql/photo
    """
    interface.implements(interfaces.IPhoto)

    def __init__(self, struct):
        self.title=struct['name']
        self.id=str(struct['id']) #it s the facebook unique id of the photo
        self.thumb_url = str(struct['picture'])
        self.url = str(struct['source'])
        self.description = u''
        
        #extra from facebook
        #self.position = struct['position']
        self.width=struct['width']
        self.height=struct['height']
        
        self.medium = str(struct['images'][1]['source'])
        self.light = str(struct['images'][2]['source'])
    
