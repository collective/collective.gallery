import unittest2 as unittest
from plone.app import testing
from collective.gallery.tests import layer

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
