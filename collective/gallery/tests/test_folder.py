import unittest
from collective.gallery import folder
from collective.gallery.tests import utils
from zope.publisher.browser import TestRequest as Request

folder.BaseFolderView.catalog = utils.FakeCatalog()

class Test(unittest.TestCase):
    
    def setUp(self):
        self.context = utils.FakeContext()
        self.request = Request()
        utils.make_request_annotable(self.request)
        folder.BaseFolderView.pp = property(utils.fake_get_property)
        self.view = folder.BaseFolderView(self.context, self.request)

    def testPhotos(self):
    
        # vipod (from irc channel): temporary fix to show IAnnotations problem:
        # default IAnnotations adapter wasn't registered so I'm registering it
        # here by manually including zope.annotation configuration,
        # actually imgs() method uses too many plone functions, so to override
        # all this behaviour you'll also need to patch getToolByName which is
        # used by this method, thus I think it'd be easier to implement this
        # testcase as integrational, inherited from PloneTestCase
        from Products.Five import zcml
        import zope.component
        import zope.annotation
        zcml.load_config('meta.zcml', zope.component)
        zcml.load_config('configure.zcml', zope.annotation)
        
        
        imgs = self.view.photos()
        self.assertEqual(len(imgs), 2)

        for img in imgs:
            test, msg = utils.verifyImage(img)
            self.failUnless(test, msg)

def test_suite():
    """This sets up a test suite that actually runs the tests in the class
    above
    """
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(Test))
    return suite
