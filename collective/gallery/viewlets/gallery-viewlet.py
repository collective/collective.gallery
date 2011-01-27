from zope import component
from zope import interface
from plone.app.layout.viewlets import common
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile

from collective.gallery import interfaces

class Link(object):
    interface.implements(interfaces.ILink)
    def __init__(self, url):
        self.url = url
        
    def getRemoteUrl(self):
        return self.url

class GalleryViewlet(common.ViewletBase):
    """Gallery viewlet"""
    interface.implements(interfaces.IGallery)
    index = ViewPageTemplateFile('gallery-viewlet.pt')

    def __init__(self, context, request, view, manager=None):
        super(GalleryViewlet, self).__init__(context, request, view,
                                             manager=manager)
        self.gallery = None
        #TODO: fecth from propertymanager a property with a link or a path
        #First try with a link
        self.gallerycontext = Link(self.context.getProperty('gallery'))
        try:
            self.gallery = component.getMultiAdapter((self.gallerycontext, self.request),
                                                 interfaces.IGallery,
                                                 name="gallery")
        except component.ComponentLookupError,e:
            pass
        self.id = ''
        self.title = ''
        self.creator = ''
        self.description = ''
        self.date = ''

    def validate(self):
        return True

    def photos(self):
        if self.gallery is not None:
            return self.gallery.photos()
        return []
