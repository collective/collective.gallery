"""This is an integration "unit" test. It uses PloneTestCase, but does not
use doctest syntax.

You will find lots of examples of this type of test in CMFPlone/tests, for 
example.
"""

from collective.gallery.tests import base

class TestSetup(base.TestCase):
    """The name of the class should be meaningful. This may be a class that
    tests the installation of a particular product.
    """

    def setUp(self):
        super(TestSetup, self).setUp()
        self.portal_types = self.portal.portal_types

    def beforeTearDown(self):
        pass

    def test_view_methods(self):
        for t in ('Link', 'Folder', 'Topic'):
            views = self.portal_types.getTypeInfo(t).view_methods
            self.failUnless("gallery.html" in views,
                            'gallery.html not in views of %s'%t)

    def test_properties(self):
        pp = self.portal.portal_properties.gallery_properties
        self.failUnless(hasattr(pp, 'photo_max_size'))
        self.failUnless(pp.photo_max_size == 400)
        self.failUnless(type(pp.photo_max_size) == int)
        self.failUnless(hasattr(pp, 'thumb_max_size'))
        self.failUnless(type(pp.thumb_max_size) == int)

def test_suite():
   return base.build_test_suite((TestSetup,))
