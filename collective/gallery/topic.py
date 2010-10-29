from collective.gallery import interfaces
from collective.gallery import cache
from collective.gallery import folder
from collective.gallery import core
from plone.memoize import ram
from zope import interface

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
            results.append(folder.Photo(photo))

        return results
