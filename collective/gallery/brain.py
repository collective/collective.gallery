from zope import component
from zope import interface
from Products.ZCatalog.interfaces import ICatalogBrain

from collective.gallery import interfaces

class Photo(object):
    """Photo implementation from brain"""
    interface.implements(interfaces.IPhoto)
    component.adapts(ICatalogBrain)

    def __init__(self, brain):
        self.id = brain.getId
        self.url = brain.getURL()
        self.thumb_url = self.url + self.thumb_url_suffix()
        self.title = brain.Title
        self.description = brain.Description

    def thumb_url_suffix(self):
        return '/image_thumb'
