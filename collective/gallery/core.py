from Products.Five import BrowserView
from collective.gallery import interfaces
from plone.memoize import view
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
        return self.pp.gallery_properties.photo_max_size

    @property
    def height(self):
        return self.pp.gallery_properties.photo_max_size

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
    
    @property
    @view.memoize_contextless
    def pp(self):
        return getToolByName(self.context, 'portal_properties')

    def search(self, query):
        return []
    
    def add(self, photos):
        pass

    def photos(self):
        return []

def sizes(available_sizes, asked_size):
    """Returns size (width,height) to ask to services to best fit with the UI.
    
    * available sizes must be an ordered list of sizes (width,height)
    * asked_size is the size ask by the template or the site properties
    """
    asked_width, asked_height = asked_size
    asked_width = int(asked_width)
    asked_height = int(asked_height)
    minus_size = None
    
    while asked_width != 0 or asked_height != 0:
        for w,h in available_sizes:
            w = int(w); h = int(h)
            if w>asked_width or h>asked_height:
                continue
            else:
                minus_size = str(w),str(h)
                break
        asked_width = asked_width - 1
        asked_height = asked_height -1
    
    return minus_size
