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
            self.failUnless("galleriffic" in views, 'gallery not in views of %s'%t)

    def test_properties(self):
        site_pp = self.portal.portal_properties.site_properties
        self.failUnless(hasattr(site_pp, 'gallery_width'))
        self.failUnless(hasattr(site_pp, 'gallery_height'))
        self.failUnless(site_pp.gallery_width == 400)
        self.failUnless(site_pp.gallery_height == 400)

def test_suite():
    """This sets up a test suite that actually runs the tests in the class
    above
    """
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(TestSetup))
    return suite
