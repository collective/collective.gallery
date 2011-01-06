import unittest
from collective.gallery.tests import base
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

    def testCreator2(self):
        self.failUnless(self.view.creator == self.view.context.Creators()[0])

class TestIntegration(base.TestCase):

    def setUp(self):
        super(TestIntegration, self).setUp()
        self.folder.invokeFactory(id='mylink', type_name='Link')
        self.link = self.folder.mylink
        self.link.setRemoteUrl('http://notsupported.com/agallery')

    def testProperties(self):
        view = self.link.unrestrictedTraverse('@@gallery')
        self.failUnless(view.width == 400)
        self.portal.portal_properties.gallery_properties._updateProperty('photo_max_size', 500)

        self.failUnless(view.width == 500)

def test_suite():
    """This sets up a test suite that actually runs the tests in the class
    above
    """
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(Test))
    suite.addTest(unittest.makeSuite(TestIntegration))
    return suite
