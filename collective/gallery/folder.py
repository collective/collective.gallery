from zope import component
from zope import interface

from collective.gallery import brain
from collective.gallery import interfaces
from collective.gallery import core

class BaseFolderView(core.BaseBrowserView):
    """A base gallery view"""
    interface.implements(interfaces.IGallery)

    def photos(self):
        return map(self._brainToPhoto, self._extract_objects())

    def _extract_objects(self):
        contentFilter = {'portal_type':'Image'}
        return self.context.getFolderContents(contentFilter)

    def _brainToPhoto(self, ob):
        try:
            photo = interfaces.IPhoto(ob)
        except component.ComponentLookupError,e :
            photo = brain.Photo(ob)
        return photo
