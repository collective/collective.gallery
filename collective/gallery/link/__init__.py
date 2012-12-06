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
from collective.gallery.link.base import BaseResource
from Products.statusmessages.interfaces import IStatusMessage

from collective.gallery.link.facebook  import check as check_facebook
from collective.gallery.link.flickr    import check as check_flickr
from collective.gallery.link.picasaweb import check as check_picasaweb

from collective.gallery.link.facebook  import Link as FacebookLink
from collective.gallery.link.flickr    import Link as FlickrLink
from collective.gallery.link.picasaweb import Link as PicasawebLink

class BaseLinkView(core.BaseBrowserView):
    """A base browser view for link content type"""
    interface.implements(interfaces.IGallery)

    def __init__(self, context, request):
        super(BaseLinkView, self).__init__(context, request)
        self.url = self.context.getRemoteUrl()
        self.resource = None
        self._baseresource = BaseResource(self.context)
#        self._resource()

    def __call__(self):
        self.update()
        return self
#        return self.index()

    def update(self):
        """Return the first component find that is valid for this context.
        If none are found use a dummy ressource"""

        if self.resource is None:
            url = self.url
            #to optimize performance those are hardcoded
            if check_facebook(url):
                self.resource = FacebookLink(self.context)
            elif check_picasaweb(url):
                self.resource = PicasawebLink(self.context)
            elif check_flickr(url):
                self.resource = FlickrLink(self.context)

        if self.resource is None:
            resources = component.getAdapters((self.context,),
                                              interfaces.IGallery)
            for name,r in resources:
                #every adapters should have a validate method
                if r.validate():
                    self.resource = r
                    break

        if self.resource:
            self.resource.width = self.width
            self.resource.height = self.height
        else:
            msg = i18n.message_no_backend_for_link
            self.addmessage(msg, type=u"error")

    def addmessage(self, message, type=u"info"):
        try:
            IStatusMessage(self.request).addStatusMessage(message, type=type)
        except TypeError:
            pass

#    @ram.cache(cache.cache_key)
    def photos(self):
        resource = self.resource
        if resource is None:
            resource = self._baseresource
        return resource.photos()

    @property
    def creator(self):
        resource = self.resource
        if resource is None:
            resource = self._baseresource
        return resource.creator

    @property
    def title(self):
        resource = self.resource
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
