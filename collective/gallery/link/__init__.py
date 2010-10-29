from collective.gallery import interfaces
from collective.gallery import cache
from collective.gallery import core
from plone.memoize import ram
from urlparse import urlsplit
from urllib import quote
from zope import component
from zope import interface

class BaseLinkView(core.BaseBrowserView):
    """A base browser view for link content type"""
    interface.implements(interfaces.IGallery)

    def __init__(self, context, request):
        super(BaseLinkView, self).__init__(context, request)
        self.url = self.context.getRemoteUrl()
        self.resource = None

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
            if not self.resource:
                self.resource = DummyResource()
        self.resource.width = self.width
        self.resource.height = self.height
        return self.resource

    @ram.cache(cache.cache_key)
    def photos(self):
        resource = self._resource()
        return resource.photos()

    @property
    def creator(self):
        resource = self._resource()
        return resource.creator
    
    @property
    def title(self):
        resource = self._resource()
        return resource.title

    def search(self, query):
        resource = self._resource()
        return resource.search(query)

    
    def add(self, photos):
        resource = self._resource()
        resource.add(photos)


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


class DummyResource(object):
    """An IGallery that return nothing, but add a msg"""
    interface.implements(interfaces.IGallery)

    def __init__(self):
        self.creator = ''
        self.title = ''

    def photos(self):
        return []
