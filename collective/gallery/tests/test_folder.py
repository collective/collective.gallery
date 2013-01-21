from collective.gallery.tests import base
from collective.gallery.tests import utils


class UnitTestFolder(base.UnitTestCase):

    def setUp(self):
        super(UnitTestFolder, self).setUp()
        from collective.gallery import folder
        self.view = folder.BaseFolderView(self.context, self.request)
        self.view.settings = utils.FakeProperty
        self.view._brainToPhoto = utils.brainToPhoto

    def testPhotos(self):

        # vipod (from irc channel): temporary fix to show IAnnotations problem:
        # default IAnnotations adapter wasn't registered so I'm registering it
        # here by manually including zope.annotation configuration,
        # actually imgs() method uses too many plone functions, so to override
        # all this behaviour you'll also need to patch getToolByName which is
        # used by this method, thus I think it'd be easier to implement this
        # testcase as integrational, inherited from PloneTestCase
        try:
            from Zope2.App.zcml import load_config
        except ImportError:
            from Products.Five.zcml import load_config
        import zope.component
        import zope.annotation

        load_config('meta.zcml', zope.component)
        load_config('configure.zcml', zope.annotation)

        imgs = self.view.photos()
        self.assertEqual(len(imgs), 2)

        for img in imgs:
            test, msg = utils.verifyImage(img)
            self.assertTrue(test, msg)


class TestIntegration(base.TestCase):
    pass
