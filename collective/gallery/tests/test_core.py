import unittest
from collective.gallery.tests import base

class Test(unittest.TestCase):

    def setUp(self):
        from collective.gallery import core
        from collective.gallery.tests import utils
        from ZPublisher.tests.testPublish import Request

        self.context = utils.FakeContext()
        self.request = Request()
        self.view = core.BaseBrowserView(self.context, self.request)

    def testTitle(self):
        self.assertEqual(self.view.title, "a title")

    def testCreator(self):
        self.assertEqual(self.view.creator, "myself")

    def testDescription(self):
        self.assertEqual(self.view.description, "a description")

    def testDate(self):
        self.assertEqual(self.view.date, "a date")

    def testPhotos(self):
        self.failUnless(not self.view.photos())
        self.assertEqual(type(self.view.photos()), list)

class TestIntegration(base.TestCase):

    def testProperties(self):
        view = self.portal.unrestrictedTraverse('@@gallery')
        self.failUnless(view.width == 400)
        self.portal.portal_properties.gallery_properties._updateProperty('photo_max_size', 500)
        self.failUnless(view.width == 500)

def test_suite():
    """This sets up a test suite that actually runs the tests in the class
    above
    """
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(Test))
    return suite
