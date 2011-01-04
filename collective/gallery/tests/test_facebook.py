import unittest

URL1 = "http://www.facebook.com/album.php?aid=177781&id=275081154800" #put a url that is supposed to work
from collective.gallery.tests import utils

class Test(unittest.TestCase):

    def setUp(self):
        self.adapter = self.getAdapter(URL1)

    def getAdapter(self, url):
        from collective.gallery.link import facebook
        return facebook.Link(utils.FakeLink(url))

    def testDefaultWithHeight(self):
        #test default values
        self.failUnless(self.adapter.width == 400)
        self.failUnless(self.adapter.height == 400)
    
    def testValidate(self):
        self.failUnless(self.adapter.validate())
        adapter = self.getAdapter(URL1)
        self.failUnless(adapter.validate())
        adapter = self.getAdapter("http://no.facebook.com")
        self.failUnless(not adapter.validate())

    def testCreator(self):
        pass #not arelady supported
    
    def testPhotos(self):
        imgs = self.adapter.photos()
        for img in imgs:
            test, msg = utils.verifyImage(img)
            self.failUnless(test, msg)
        self.failUnless(len(imgs)==50)

def test_suite():
    """This sets up a test suite that actually runs the tests in the class
    above
    """
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(Test))
    return suite
