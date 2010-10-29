import unittest
from collective.gallery.link import picasaweb
from collective.gallery.tests import utils

NONAUTH_URL = 'http://picasaweb.google.fr/ceronjeanpierre/PhotosTriEsDuMariage'
AUTH_URL = 'http://picasaweb.google.com/toutpt/20091116ConcertDeRammstein?authkey=Gv1sRgCN2i5uS0y5_lLQ#'

class Test(unittest.TestCase):

    def setUp(self):
        self.adapter = self.getAdapter(NONAUTH_URL)

    def getAdapter(self, url):
        return picasaweb.Link(utils.FakeLink(url))

    def testDefaultWithHeight(self):
        #test default values
        self.failUnless(self.adapter.width == 400)
        self.failUnless(self.adapter.height == 400)
    
    def testValidate(self):
        self.failUnless(self.adapter.validate())
        adapter = self.getAdapter(AUTH_URL)
        self.failUnless(adapter.validate())
        adapter = self.getAdapter("http://nopicasa.google.com")
        self.failUnless(not adapter.validate())

    def testCreator(self):
        self.failUnless(self.adapter.creator == "ceronjeanpierre")
    
    def testAuthKey(self):
        self.failUnless(not self.adapter.authkey)
        adapter = self.getAdapter(AUTH_URL)
        self.failUnless(adapter.authkey)

    def test_imgmax(self):
        imgmax = self.adapter.imgmax(400, 300)
        self.assertEqual(imgmax, 288)


    def testPhotosNonAuth(self):
        imgs = self.adapter.photos()
        for img in imgs:
            test, msg = utils.verifyImage(img)
            self.failUnless(test, msg)

    def testPhotosAuth(self):
        adapter = self.getAdapter(AUTH_URL)
        imgs = adapter.photos()
        for img in imgs:
            test, msg = utils.verifyImage(img)
            self.failUnless(test, msg)

    def testImgsWrongURL(self):
        adapter = self.getAdapter("http://notpicasaweb.com")
        msg = "API not respected"
        self.failUnless(not adapter.creator, msg)
        self.failUnless(not adapter.albumName, msg)
        self.failUnless(not adapter.photos(), msg)
        self.failUnless(type(adapter.photos()) == list, msg)

def test_suite():
    """This sets up a test suite that actually runs the tests in the class
    above
    """
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(Test))
    return suite
