import unittest

#from zope.testing import doctestunit
#from zope.component import testing
from Testing import ZopeTestCase as ztc

try:
    from Zope2.App import zcml
    from OFS import metaconfigure
    zcml # pyflakes
    metaconfigure
except ImportError:
    from Products.Five import zcml
    from Products.Five import fiveconfigure as metaconfigure

from Products.PloneTestCase import PloneTestCase as ptc
from Products.PloneTestCase.layer import PloneSite
from Testing.ZopeTestCase import installPackage, installProduct

ptc.setupPloneSite(extension_profiles=('collective.gallery:default',))

class Layer(PloneSite):

    @classmethod
    def setUp(cls):
        metaconfigure.debug_mode = True
        import collective.gallery
        zcml.load_config('configure.zcml', collective.gallery)
        metaconfigure.debug_mode = False
        installPackage('collective.gallery', quiet=True)

    @classmethod
    def tearDown(cls):
        pass

def remove_statusmessage():
    #monkey patch to remove statusmessage dependency
    from collective.gallery import link
    def addmessage(message, type=u"info"):pass
    link.BaseLinkView.addmessage = addmessage


class TestCase(ptc.PloneTestCase):

    layer = Layer

    def afterSetUp(self):
        remove_statusmessage()

class FunctionalTestCase(ptc.FunctionalTestCase):
    
    layer = Layer

    def afterSetUp(self):
        remove_statusmessage()
