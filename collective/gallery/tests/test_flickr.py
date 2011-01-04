import unittest
from collective.gallery.tests import utils

URL_SETS_PUBLIC = 'http://www.flickr.com/photos/princeofnorway/sets/72157622650234713/'

class Test(unittest.TestCase):

    def setUp(self):
        self.fakelink = utils.FakeLink(URL_SETS_PUBLIC)
        self.adapter = self.getAdapter()

    def getAdapter(self, link=None):
        if not link:
            link = self.fakelink
        from collective.gallery.link import flickr
        return flickr.Link(link)

    def testDefaultWithHeight(self):
        self.failUnless(self.adapter.width == 400)
        self.failUnless(self.adapter.height == 400)
    
    def testValidate(self):
        self.failUnless(self.adapter.validate())
        self.fakelink.remoteUrl = "http://not.flickr.com"
        adapter = self.getAdapter()
        self.failUnless(not adapter.validate())

    def testCreator(self):
        self.failUnless(self.adapter.creator == "CJsarp")

    def testUserInfo(self):
        user_info = self.adapter.user_info
        self.failUnless(user_info['user_id']=="41300176@N02")
        self.failUnless(user_info['username']=="CJsarp")
        self.failUnless(user_info['user_yahooaccount']=="princeofnorway")

    def testPhotos(self):
        imgs = self.adapter.photos()
        for img in imgs:
            test, msg = utils.verifyImage(img)
            self.failUnless(test, msg)

    def testNotValideURL(self):
        url = 'http://nota.flickr.com/url'
        fakelink = utils.FakeLink(url)
        fakelink._modified = "updated"
        adapter = self.getAdapter(link=fakelink)
        self.failUnless(not adapter.creator, adapter.creator)
        self.failUnless(not adapter.photos())


def test_suite():
    """This sets up a test suite that actually runs the tests in the class
    above
    """
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(Test))
    return suite
