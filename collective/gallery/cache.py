from time import time


def cache_key(fun, self):
    """We are making cache key on
    * modification date
    * one hour
    * width and height of the view
    * len(object.getIds) if exists
    """
    mod_date = str(self.context.modified())
    one_hour = str(time() // (60 * 60))
    objectIds = ""
    if hasattr(self.context.aq_inner.aq_explicit, 'objectIds'):
        objectIds = str(len(self.context.aq_inner.aq_explicit.objectIds()))
    return mod_date + one_hour + objectIds


def url_cache_key(fun, self):
    return cache_key(fun, self) + "_%s" % self.url
