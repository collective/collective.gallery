from zope import component
from zope import interface

from collective.gallery import interfaces

from Products.CMFCore.utils import getToolByName
from plone.registry.interfaces import IRegistry

class BaseResource(object):
    """An IGallery base for all link services
    
    """
    interface.implements(interfaces.IGallery)
    component.adapts(interfaces.ILink)

    def __init__(self, context):
        self.context = context
        self.url = context.getRemoteUrl()
        self._width = None
        self._height = None
        self._settings = None

    def get_width(self):
        if not self._width:
            return self.settings().photo_max_size
        return self._width

    def set_width(self, value):
        self._width = value

    width = property(get_width, set_width)

    def get_height(self):
        if not self._height:
            return self.settings().photo_max_size
        return self._height

    def set_height(self, value):
        self._height = value

    height = property(get_height, set_height)

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
