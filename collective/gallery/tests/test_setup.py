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

    def testRegistry(self):
        from collective.gallery.interfaces import IGallerySettings
        pp = self.portal.portal_registry.forInterface(IGallerySettings)
        self.assertTrue(hasattr(pp, 'photo_max_size'))
        self.assertTrue(pp.photo_max_size == 400)
        self.assertTrue(type(pp.photo_max_size) == int)

