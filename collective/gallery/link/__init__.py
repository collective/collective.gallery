from urlparse import urlsplit
from urllib import quote

from zope import component
from zope import interface

from plone.memoize import ram

from Products.CMFCore.utils import getToolByName

from collective.gallery import interfaces
from collective.gallery import i18n
from collective.gallery import cache
from collective.gallery import core
from Products.statusmessages.interfaces import IStatusMessage

class BaseLinkView(core.BaseBrowserView):
    """A base browser view for link content type"""
    interface.implements(interfaces.IGallery)

    def __init__(self, context, request):
        super(BaseLinkView, self).__init__(context, request)
        self.url = self.context.getRemoteUrl()
        self.resource = None
        self._baseresource = BaseResource(self.context)
        self._resource()

    def _resource(self):
        """Return the first component find that is valid for this context.
        If none are found use a dummy ressource"""
        if not self.resource:
            resources = component.getAdapters((self.context,),
                                              interfaces.IGallery)
            for name,r in resources:
                if r.validate():
                    self.resource = r
                    break

            if self.resource:
                self.resource.width = self.width
                self.resource.height = self.height
            else:
                msg = i18n.message_no_backend_for_link
                self.addmessage(msg, type=u"error")

        return self.resource

    def addmessage(self, message, type=u"info"):
        try:
            IStatusMessage(self.request).addStatusMessage(message, type=type)
        except TypeError:
            pass

    @ram.cache(cache.cache_key)
    def photos(self):
        resource = self._resource()
        if resource is None:
            resource = self._baseresource
        return resource.photos()

    @property
    def creator(self):
        resource = self._resource()
        if resource is None:
            resource = self._baseresource
        return resource.creator

    @property
    def title(self):
        resource = self._resource()
        if resource is None:
            resource = self._baseresource
        return resource.title

    def break_url(self):
        """Taken from p4a.videoembed to be used as utility in template
        """
        # Splits and encodes the url, and breaks the query string into a dict
        url = self.url
        proto, host, path, query, fragment = urlsplit(url)
        path = quote(path)
        query = quote(query, safe='&=')
        fragment = quote(fragment, safe='')
        query_elems = {}
        # Put the query elems in a dict
        for pair in query.split('&'):
            pos = pair.find('=')
            if pos > -1:
                key = pair[:pos]
                value = pair[pos+1:]
            else:
                key = pair
                value = ''
            if key:
                query_elems[key] = value
        return host, path, query_elems, fragment


class BaseResource(object):
    """An IGallery base for all link services"""
    interface.implements(interfaces.IGallery)
    component.adapts(interfaces.ILink)

    def __init__(self, context):
        self.context = context
        self.url = context.getRemoteUrl()
        def validator(url):return False
        self.validator = validator
        self._width = None
        self._height = None

    def validate(self):
        return self.validator(self.url)

    def get_width(self):
        if not self._width:
            return self.settings().getProperty('photo_max_size', 400)
        return self._width

    def set_width(self, value):
        self._width = value

    width = property(get_width, set_width)

    def get_height(self):
        if not self._height:
            return self.settings().getProperty('photo_max_size', 400)
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
        return getToolByName(self.context, 'portal_properties').gallery_properties

    def photos(self):
        return []
