from collective.gallery import interfaces
from collective.gallery import cache
from collective.gallery import core
from plone.memoize import ram
from plone.memoize import view
from Products.CMFCore.utils import getToolByName
from zope import interface

class BaseFolderView(core.BaseBrowserView):
    """A base gallery view"""
    interface.implements(interfaces.IGallery)

    def __init__(self, context, request):
        super(BaseFolderView, self).__init__(context, request)

    @ram.cache(cache.cache_key)
    def photos(self):
        results = []
        path='/'.join(self.context.getPhysicalPath())
        photos = self.catalog.searchResults(path=path, portal_type="Image")

        for photo in photos:
            results.append(Photo(photo))

        return results

    @property
    @view.memoize_contextless
    def catalog(self):
        return getToolByName(self.context, 'portal_catalog')


class Photo(object):
    """Photo implementation from brain"""

    interface.implements(interfaces.IPhoto)

    def __init__(self, brain):
        self.id = brain.getId
        self.url = brain.getURL()
        self.thumb_url = brain.getURL() + '/image_thumb' #need to use image_thumb
        self.title = brain.Title
        self.description = brain.Description
