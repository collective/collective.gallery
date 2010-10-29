from zope.interface import directlyProvides
from zope.annotation.interfaces import IAttributeAnnotatable

def verifyImage(image):
    """Return True if image respect the interface, return false otherwise"""
    tests = []
    attrs = ('title', 'description', 'url', 'thumb_url', 'exif')
    for attr in attrs:
        if not hasattr(image, attr):
            return False, "has no %s attribute"%attr
    for attr in attrs:
        if attr == "exif":continue
        if not type(getattr(image, attr)) == str:
            return False, "%s is not a string"%attr
    return True, ""


class FakeAcquisition(object):
    def __init__(self):
        self.aq_explicit = None

class FakeContext(object):

    def __init__(self):
        self.title = "a title"
        self.description = "a description"
        self.creators = ["myself"]
        self.date="a date"
        self.aq_inner = FakeAcquisition()
        self.aq_inner.aq_explicit = self

    def Title(self):
        return self.title

    def Creators(self):
        return self.creators

    def Description(self):
        return self.description

    def Date(self):
        return self.date

    def modified(self):
        return "a modification date"

    def getPhysicalPath(self):
        return ('/','a','not','existing','path')

class FakeTopic(FakeContext):
    def queryCatalog(self, **kwargs):
        catalog = FakeCatalog()
        return catalog.searchResults()

class FakeLink(FakeContext):
    def __init__(self, url=""):
        super(FakeLink, self).__init__()
        self.remoteUrl = url
    
    def getRemoteUrl(self):
        return self.remoteUrl

    def modified(self):
        return "a modification date"

class FakeBrain(object):
    def __init__(self):
        self.Title = ""
        self.Description = ""

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

def make_request_annotable(request):
    directlyProvides(request, IAttributeAnnotatable)

class FakeProperty(object):
    def __init__(self):
        class Gallery:
            def __init__(self):
                self.gallery_width = 400
                self.gallery_height = 400
        self.site_properties = Gallery()

def fake_get_property(self):
    return FakeProperty()
