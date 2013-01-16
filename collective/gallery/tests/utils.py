

def brainToPhoto(ob):
    from collective.gallery import brain
    return brain.Photo(ob)


def verifyImage(image):
    """Return True if image respect the interface, return false otherwise"""
    attrs = ('id', 'title', 'description', 'url', 'thumb_url')
    for attr in attrs:
        if not hasattr(image, attr):
            return False, "has no %s attribute" % attr
    for attr in attrs:
        if type(getattr(image, attr)) not in (str, unicode):
            return False, "%s is not a string or unicode" % attr
    return True, ""


class FakeAcquisition(object):
    def __init__(self):
        self.aq_explicit = None


class FakeContext(object):

    def __init__(self):
        self.id = "myid"
        self.title = "a title"
        self.description = "a description"
        self.creators = ["myself"]
        self.date = "a date"
        self.aq_inner = FakeAcquisition()
        self.aq_inner.aq_explicit = self
        self._modified = "modified date"
        self.remoteUrl = ''  # fake Link

    def getId(self):
        return self.id

    def Title(self):
        return self.title

    def Creators(self):
        return self.creators

    def Description(self):
        return self.description

    def Date(self):
        return self.date

    def modified(self):
        return self._modified

    def getPhysicalPath(self):
        return ('/', 'a', 'not', 'existing', 'path')

    def getFolderContents(self, filter=None):
        catalog = FakeCatalog()
        return catalog.searchResults()

    def absolute_url(self):
        return "http://nohost.com/" + self.id

    def queryCatalog(self, **kwargs):  # fake Topic
        catalog = FakeCatalog()
        return catalog.searchResults()

    def getRemoteUrl(self):  # fake Link
        return self.remoteUrl


class FakeBrain(object):
    def __init__(self):
        self.Title = ""
        self.Description = ""
        self.getId = ""
        self.portal_type = ""

    def getURL(self):
        return "http://fakebrain.com"

    def getObject(self):
        ob = FakeContext()
        ob.title = self.Title

        return ob


class FakeCatalog(object):
    def searchResults(self, **kwargs):
        brain1 = FakeBrain()
        brain1.Title = "My first article"
        brain2 = FakeBrain()
        brain2.Title = "A great event"
        brain2.Description = "you will drink lots of beer"
        return [brain1, brain2]

    def modified(self):
        return '654654654654'


class FakeProperty(object):
    def __init__(self):
        self.photo_max_size = 400
        self.thumb_max_size = 80

    def getProperty(self, name, default=None):
        return getattr(self, name, default)


def fake_get_property(self):
    return FakeProperty()
