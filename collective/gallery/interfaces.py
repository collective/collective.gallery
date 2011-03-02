from zope import interface
from zope import schema

from collective.gallery import messageFactory as _

class IGalleryLayer(interface.Interface):
    """Browser layer"""

class IPhoto(interface.Interface):
    """Metadatas schema of a photo"""

    id = schema.ASCIILine(title=_(u"label_photo_id", default=u"Id"))

    title = schema.TextLine(title=_(u"label_photo_title", default=u"Title"))

    description = schema.TextLine(title=_(u"label_photo_description",
                                          default=u"Description"))

    url = schema.TextLine(title=_(u"label_photo_url", default=u"Source URL"))

    thumb_url = schema.TextLine(title=_(u"label_photo_thumb",
                                        default=u"Thumb source URL"))

class IGallery(interface.Interface):
    """A gallery is the business component of collective.gallery. A gallery
    manage a set of photos. The schema contains classic dublin core

    """

    id = schema.ASCIILine(title=_(u"Id"))

    title = schema.TextLine(title=_(u"Title"))

    creator = schema.TextLine(title=_(u"Author"))

    description = schema.TextLine(title=_(u"Description"))

    date = schema.Date(title=_(u"Date"))

    def photos(scale="default"):
        """Return the list of all IPhoto contained in the gallery"""

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
    from plone.app.folder.folder import IATUnifiedFolder          as IFolder
    from Products.ATContentTypes.interfaces.link import IATLink   as ILink
    from Products.ATContentTypes.interfaces.topic import IATTopic as ITopic
    from Products.ATContentTypes.interfaces.image import IATImage as IImage
    from Products.ZCatalog.interfaces import ICatalogBrain
except ImportError, e:
    from collective.gallery import logger
    logger.info('BBB: switch to plone3 %s'%e)
    #plone3
    from Products.ATContentTypes.interface import IATFolder as IFolder
    from Products.ATContentTypes.interface import IATLink   as ILink
    from Products.ATContentTypes.interface import IATTopic  as ITopic
    from Products.ATContentTypes.interface import IATImage  as IImage
    class ICatalogBrain(interface.Interface):
        pass
