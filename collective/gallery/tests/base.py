"""Test setup for integration and functional tests."""

import sys
from Products.Five import zcml
from Products.Five import fiveconfigure

from Testing import ZopeTestCase as ztc
from Products.PloneTestCase import PloneTestCase as ptc
from Products.PloneTestCase.layer import onsetup

@onsetup
def setup_addon():
    fiveconfigure.debug_mode = True
    import collective.gallery
    zcml.load_config('configure.zcml', collective.gallery)
    fiveconfigure.debug_mode = False
    ztc.installPackage('collective.gallery')

setup_addon()
ptc.setupPloneSite(extension_profiles=['collective.gallery:default'])

class GalleryTestCase(ptc.PloneTestCase):
    """We use this base class for all the tests in this package. If necessary,
    we can put common utility or setup code in here. This applies to unit 
    test cases.
    """


class GalleryFunctionalTestCase(ptc.FunctionalTestCase):
    """We use this class for functional integration tests that use doctest
    syntax. Again, we can put basic common utility or setup code in here.
    """

