from collective.gallery import interfaces
from collective.gallery import cache
from collective.gallery import core
from plone.memoize import ram
from plone.memoize import view
from Products.CMFCore.utils import getToolByName
from Products.CMFCore.interfaces import IPropertiesTool
from zope import interface
from zope import component
from Products.ATContentTypes.interfaces.image import IATImage

class BaseFolderView(core.BaseBrowserView):
    """A base gallery view"""
    interface.implements(interfaces.IGallery)

    def __init__(self, context, request):
        super(BaseFolderView, self).__init__(context, request)

    def photos(self):
        results = []
        for ob in self.context.objectValues():
            try:
                photo = interfaces.IPhoto(ob)
            except component.ComponentLookupError:
                pass
            results.append(photo)
        return results

class Photo(object):
    """Photo implementation from brain"""
    interface.implements(interfaces.IPhoto)
    component.adapts(interfaces.IImage)

    def __init__(self, image):
        self.id = image.getId()
        self.url = image.absolute_url()
        self.thumb_url = self.url + '/image_thumb' #need to use image_thumb
        self.title = image.Title()
        self.description = image.Description()
