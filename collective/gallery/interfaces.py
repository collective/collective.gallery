from zope import interface
from zope import schema
from collective.gallery import _
from plone.app.layout.globals.interfaces import IViewView

from plone.app.imaging.interfaces import IImageScale

class IPhoto(IImageScale):
    """Metadatas schema of a photo"""

    title = schema.TextLine(title=_(u"Title"))

    description = schema.TextLine(title=_(u"Description"))

    url = schema.TextLine(title=_(u"Source URL"))

    thumb_url = schema.TextLine(title=_(u"Thumb source URL"))

class IGallery(interface.Interface):
    """A gallery is the business component of collective.gallery. A gallery
    manage a set of photos. The schema contains classic dublin core
    
    """

    title = schema.TextLine(title=_(u"Title"))

    creator = schema.TextLine(title=_(u"Author"))

    description = schema.TextLine(title=_(u"Description"))

    date = schema.Date(title=_(u"Date"))

    def photos(scale="default"):
        """Return the list of all IPhoto contained in the gallery"""

#dependencies
try:
    #plone4
    from Products.ATContentTypes.interfaces.link import IATLink
except:
    #plone3
    from Products.ATContentTypes.interface.link import IATLink
