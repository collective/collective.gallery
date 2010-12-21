"""This is an integration "unit" test. It uses PloneTestCase, but does not
use doctest syntax.

You will find lots of examples of this type of test in CMFPlone/tests, for 
example.
"""

import unittest
from collective.gallery.tests.base import GalleryTestCase

from Products.CMFCore.utils import getToolByName

class TestSetup(GalleryTestCase):
    """The name of the class should be meaningful. This may be a class that
    tests the installation of a particular product.
    """

    def afterSetUp(self):
        self.portal_types = getToolByName(self.portal, 'portal_types')

    def beforeTearDown(self):
        pass

    def test_view_methods(self):
        for t in ('Link', 'Folder', 'Topic'):
            views = self.portal_types.getTypeInfo(t).view_methods
            self.failUnless("gallery.html" in views, 'gallery not in views of %s'%t)

    def test_properties(self):
        pp = self.portal.portal_properties.gallery_properties
        self.failUnless(hasattr(pp, 'photo_max_size'))
        self.failUnless(pp.photo_max_size == 400)
        self.failUnless(type(pp.photo_max_size) == int)
        self.failUnless(hasattr(pp, 'thumb_max_size'))
        self.failUnless(type(pp.thumb_max_size) == int)
        self.failUnless(hasattr(pp, 'numthumbs'))
        self.failUnless(type(pp.numthumbs) == int)
        self.failUnless(hasattr(pp, 'enablehistory'))
        self.failUnless(type(pp.enablehistory) == bool)

def test_suite():
    """This sets up a test suite that actually runs the tests in the class
    above
    """
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(TestSetup))
    return suite
