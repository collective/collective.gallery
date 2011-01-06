from zope import interface

from collective.gallery import core
from collective.gallery import interfaces

class BaseTopicView(core.BaseBrowserView):
    """A base topic gallery view"""
    interface.implements(interfaces.IGallery)

    def photos(self):
        return map(self._brainToPhoto, self._extract_objects())

    def _extract_objects(self):
        return self.context.queryCatalog()

    def _brainToPhoto(self, ob):
        return interfaces.IPhoto(ob)
