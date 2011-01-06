import unittest2 as unittest
from plone.app import testing
from collective.gallery.tests import layer
from collective.gallery.tests import utils

class UnitTestCase(unittest.TestCase):
    
    def setUp(self):
        from ZPublisher.tests.testPublish import Request
        super(UnitTestCase, self).setUp()
        self.context = utils.FakeContext()
        self.request = Request()
        utils.make_request_annotable(self.request)

class TestCase(unittest.TestCase):

    layer = layer.GALLERY_INTEGRATION

    def setUp(self):
        super(TestCase, self).setUp()
        self.portal = self.layer['portal']
        testing.setRoles(self.portal, testing.TEST_USER_ID, ['Manager'])
        self.portal.invokeFactory('Folder', 'test-folder')
        testing.setRoles(self.portal, testing.TEST_USER_ID, ['Member'])
        self.folder = self.portal['test-folder']

    def getGalleryView(self, context):
        return context.unrestrictedTraverse('@@gallery')

class FunctionalTestCase(unittest.TestCase):
    
    layer = layer.GALLERY_FUNCTIONAL

    def setUp(self):
        self.portal = self.layer['portal']
        testing.setRoles(self.portal, testing.TEST_USER_ID, ['Manager'])
        self.portal.invokeFactory('Folder', 'test-folder')
        testing.setRoles(self.portal, testing.TEST_USER_ID, ['Member'])
        self.folder = self.portal['test-folder']

def build_test_suite(test_classes):
    suite = unittest.TestSuite()
    for klass in test_classes:
        suite.addTest(unittest.makeSuite(klass))
    return suite

        