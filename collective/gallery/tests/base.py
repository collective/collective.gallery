from Products.PloneTestCase import PloneTestCase as ptc

from collective.gallery.tests import layer

ptc.setupPloneSite(extension_profiles=['collective.gallery:default'])

class TestCase(ptc.PloneTestCase):
    """We use this base class for all the tests in this package. If necessary,
    we can put common utility or setup code in here. This applies to unit 
    test cases.
    """

    layer = layer.Gallery


class FunctionalTestCase(ptc.FunctionalTestCase):
    """We use this class for functional integration tests that use doctest
    syntax. Again, we can put basic common utility or setup code in here.
    """

    layer = layer.Gallery
