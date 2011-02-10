from collective.portlet.itemview import vocabulary
from zope import component
from zope import interface
from collective.gallery import interfaces
from Products.Five.browser import BrowserView
import logging
logger = logging.getLogger('collective.gallery')

class GalleryPortletViewEntry(object):
    interface.implements(vocabulary.IPortletView)
    
    id = "itemview_portlet_gallery"
    name = u"Gallery"

class GalleryPortletView(BrowserView):
    interface.implements(interfaces.IGallery)

    def __init__(self, context, request):
        self.context = context
        self.request = request
        try:
            self.galleryview = component.getMultiAdapter((self.context, self.request),
                                                     name="gallery")

        except component.ComponentLookupError:
            logger.error('no gallery view for %s'%self.context)
            self.galleryview = None

        self.id = self.context.getId()
        self.title = self.context.Title()
        self.creator = self.context.Creators()[0]
        self.description = self.context.Description()

    def photos(self):
        """Return the list of all IPhoto contained in the gallery"""
        if not self.galleryview: return []
        photos = self.galleryview.photos()
        return photos

