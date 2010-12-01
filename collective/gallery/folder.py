from collective.gallery.interfaces import IGallery, IPhoto
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
    interface.implements(IGallery)

    def __init__(self, context, request):
        super(BaseFolderView, self).__init__(context, request)

    def photos(self):
        results = []
        for ob in self.context.objectValues():
            try:
                photo = IPhoto(ob)
            except component.ComponentLookupError:
                pass
            results.append(photo)
        return results

class Photo(object):
    """Photo implementation from brain"""

    interface.implements(IPhoto)
    component.adapts(IATImage)

    def __init__(self, context):
        self.context = context
        self.title = context.Title()
        self.description = context.Description()
        self.id = context.getId()
        self.url = context.absolute_url()

    @property
    def thumb_url(self):
        image = self.context.restrictedTraverse('@@image')
        scales