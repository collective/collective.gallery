from zope import interface
from zope import schema
from collective.gallery import _
from plone.app.layout.globals.interfaces import IViewView

class IExif(interface.Interface):
    """Exchangeable Image File Format standard metadatas."""

    distance = schema.TextLine(title=_(u"Exif distance"))
    exposure = schema.TextLine(title=_(u"Exposure time"))
    flash = schema.TextLine(title=_(u"Flash"))
    focallength = schema.TextLine(title=_(u"Focal length"))
    iso = schema.TextLine(title=_(u"ISO Speed"))
    make = schema.TextLine(title=_(u"Make"),
                           description=_(u"Manifacturer of image input equipement"))
    model = schema.TextLine(title=_(u"Model"),
                           description=_(u"Model of image input equipement"))
    time = schema.TextLine(title=_(u"Time"),
                           description=_(u"The date/time the photo was taken, represented as the number of milliseconds since January 1st, 1970."))

class IPhoto(interface.Interface):
    """Metadatas schema of a photo"""

    title = schema.TextLine(title=_(u"Title"))

    description = schema.TextLine(title=_(u"Description"))

    url = schema.TextLine(title=_(u"Source URL"))

    thumb_url = schema.TextLine(title=_(u"Thumb source URL"))

    exif = schema.Object(IExif)
    
    file = schema.Bytes(title=_(u"The file object"))


class IGallery(interface.Interface):
    """A gallery is the business component of collective.gallery. A gallery
    manage a set of photos. The schema contains classic dublin core
    
    """

    title = schema.TextLine(title=_(u"Title"))

    creator = schema.TextLine(title=_(u"Author"))

    description = schema.TextLine(title=_(u"Description"))

    date = schema.Date(title=_(u"Date"))

    width = schema.Int(title=_(u'Width'),
                       min=0,
                       default=400)

    height = schema.Int(title=_(u'height'),
                        min=0,
                        default=400)

    def photos():
        """Return the list of all IPhoto contained in the gallery"""

    def search(query):
        """Return a lisf of IPhoto based on the query parameter. query format
        is the same as catalog query"""
    
    def add(photos):
        """Add a list of IPhoto to add to the service
        """

class IGalleryTemplateTerm(interface.Interface):
    """Make a utility registred with this interface.
    It will be used to build the vocabularies and to make the
    rendering"""

    name = schema.TextLine(title=_(u"Name"),
                           description=_(u"The friendly name of the template")
                           )

    def template():
        """return the template (PageTemplate instance)"""

    def validate():
        """Return true/false by checking if the template can be applied to
        the context.

        Best example is picasa_slideshow with Link content type must check if
        the url is a picasa one.
        """


#dependencies
try:
    #plone4
    from Products.ATContentTypes.interfaces.link import IATLink
except:
    #plone3
    from Products.ATContentTypes.interface.link import IATLink
