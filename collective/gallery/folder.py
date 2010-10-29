from collective.gallery.interfaces import IGallery, IPhoto, IExif
from collective.gallery import cache
from collective.gallery import core
from plone.memoize import ram
from plone.memoize import view
from Products.CMFCore.utils import getToolByName
from zope import interface

class BaseFolderView(core.BaseBrowserView):
    """A base gallery view"""
    interface.implements(IGallery)

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

    interface.implements(IPhoto)

    def __init__(self, brain):
        self.url = brain.getURL()
        self.thumb_url = brain.getURL() + '/image_thumb' #need to use image_thumb
        self.title = brain.Title
        self.description = brain.Description
        self.exif = Exif(brain)

class Exif(object):
    """Exif metadatas"""
    interface.implements(IExif)

    def __init__(self, brain):
        ob = brain.getObject()
        if hasattr(ob, 'getEXIF'):
            self.raw_exif_data = ob.getEXIF()
        else:
            self.raw_exif_data = {}

        attrs = ('distance','exposure', 'flash', 'focallength', 'fstop',
                 'imageUniqueID', 'iso', 'make', 'model', 'time')
        for attr in attrs:
            setattr(self, attr, "")
        if self.raw_exif_data:
            #it seems exif keys depends on the image data
            self.flash = self.raw_exif_data.get("EXIF Flash", "")
            self.focallength = self.raw_exif_data.get("EXIF FocalLength","")
            self.iso = self.raw_exif_data.get("EXIF ISOSpeedRatings","")
            self.make = self.raw_exif_data.get("Image Make","")
            self.time = self.raw_exif_data.get("Image DateTime","")
