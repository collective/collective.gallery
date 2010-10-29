import unittest
from collective.gallery import link
from collective.gallery.tests import utils
from zope.publisher.browser import TestRequest as Request

class Test(unittest.TestCase):

    def setUp(self):
        request = Request()
        context = utils.FakeLink()
        utils.make_request_annotable(request)
        link.BaseLinkView.pp = property(utils.fake_get_property)
        self.adapter = link.BaseLinkView(context, request)

    def testCreator(self):
        self.failUnless(self.adapter.creator == "ceronjeanpierre")

    def testPhotos(self):
        imgs = self.adapter.photos()
        self.failUnless(not imgs)
        self.failUnless(len(imgs) == 0)

    def testCreator(self):
        self.failUnless(not self.adapter.creator, "must be empty")

def test_suite():
    """This sets up a test suite that actually runs the tests in the class
    above
    """
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(Test))
    return suite
