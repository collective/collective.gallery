from zope import component
from zope import interface

from collective.gallery import interfaces

class Photo(object):
    """Photo implementation from brain"""
    interface.implements(interfaces.IPhoto)
    component.adapts(interfaces.ICatalogBrain)

    def __init__(self, brain):
        self.id = brain.getId
        self.url = brain.getURL()
        if brain.portal_type == 'News Item':
            self.url += '/image'
        self.thumb_url = brain.getURL() + self.thumb_url_suffix()
        self.title = brain.Title
        self.description = brain.Description

    def thumb_url_suffix(self):
        return '/image_thumb'
