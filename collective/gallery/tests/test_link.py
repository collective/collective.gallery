import unittest
from collective.gallery.tests import utils
from zope.publisher.browser import TestRequest as Request

class Test(unittest.TestCase):

    def setUp(self):
        from collective.gallery import link
        request = Request()
        context = utils.FakeLink()
        utils.make_request_annotable(request)
        self.view = link.BaseLinkView(context, request)
        self.view.settings = utils.FakeProperty

    def testCreator(self):
        self.failUnless(self.view.creator == "ceronjeanpierre")

    def testPhotos(self):
        imgs = self.view.photos()
        self.failUnless(not imgs)
        self.failUnless(len(imgs) == 0)

    def testCreator(self):
        self.failUnless(not self.view.creator, "must be empty")

def test_suite():
    """This sets up a test suite that actually runs the tests in the class
    above
    """
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(Test))
    return suite
