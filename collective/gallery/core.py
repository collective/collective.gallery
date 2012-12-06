from zope import component
from zope import interface
from Products.Five import BrowserView

from Products.CMFCore.utils import getToolByName
from plone.registry.interfaces import IRegistry

from collective.gallery import interfaces


class BaseBrowserView(BrowserView):
    """This code is the base code of gallery views.

    All album metadatas are taken from the context. with and height data
    are provided by portal_properties.site_properties
    """

    interface.implements(interfaces.IGallery)

    def __init__(self, context, request):
        self.context = context
        self.request = request
        self._settings = None

    @property
    def width(self):
        return self.settings().photo_max_size

    @property
    def height(self):
        return self.settings().photo_max_size

    @property
    def id(self):
        return self.context.getId()

    @property
    def title(self):
        return self.context.Title()

    @property
    def creator(self):
        return self.context.Creators()[0]
    
    @property
    def description(self):
        return self.context.Description()

    @property
    def date(self):
        return self.context.Date()
    
    def settings(self):
        if self._settings is None:
            registry = component.getUtility(IRegistry)
            self._settings = registry.forInterface(interfaces.IGallerySettings)
        return self._settings

    def photos(self):
        return []

    def get_photo(self, index=0):
        photos = self.photos()

        if len(photos) == 0:
            return {'url':'','title':u'', 'description':u'', 'thumb_url':''}

        if index > len(self.photos()):
            if index!=0:
                index=0

        return photos[index]
