from Products.Five import BrowserView
from collective.gallery import interfaces
from zope import interface
from Products.CMFCore.utils import getToolByName

class BaseBrowserView(BrowserView):
    """This code is the base code of gallery views.

    All album metadatas are taken from the context. with and height data
    are provided by portal_properties.site_properties
    """

    interface.implements(interfaces.IGallery)

    def __init__(self, context, request):
        self.context = context
        self.request = request

    @property
    def width(self):
        return self.settings().getProperty('photo_max_size', 400)

    @property
    def height(self):
        return self.settings().getProperty('photo_max_size', 400)

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
        return getToolByName(self.context, 'portal_properties').gallery_properties

    def photos(self):
        return []
