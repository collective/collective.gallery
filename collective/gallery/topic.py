from zope import interface
from zope import component

from plone.memoize import ram

from collective.gallery import interfaces
from collective.gallery import cache
from collective.gallery import folder
from collective.gallery import core

class BaseTopicView(core.BaseBrowserView):
    """A base topic gallery view"""
    interface.implements(interfaces.IGallery)

    def __init__(self, context, request):
        super(BaseTopicView, self).__init__(context, request)

    @ram.cache(cache.cache_key)
    def photos(self):
        results = []
        photos = self.context.queryCatalog()

        for photo in photos:
            #image data are take from brain in folder implementation
            results.append(Photo(photo))

        return results


class Photo(object):
    """Photo implementation from brain"""
    interface.implements(interfaces.IPhoto)

    def __init__(self, brain):
        self.id = brain.getId
        self.url = brain.getURL()
        self.thumb_url = self.url + '/image_thumb' #need to use image_thumb
        self.title = brain.Title
        self.description = brain.Description
