from collective.gallery.tests import base
from collective.gallery.tests import utils

class Test(base.UnitTestCase):

    def setUp(self):
        super(Test, self).setUp()
        from collective.gallery import link
        self.view = link.BaseLinkView(self.context, self.request)
        self.view.settings = utils.FakeProperty

    def testPhotos(self):
        imgs = self.view.photos()
        self.failUnless(not imgs)
        self.failUnless(len(imgs) == 0)

    def testCreator(self):
        self.failUnless(self.view.creator == self.view.context.Creators()[0])

class TestIntegration(base.TestCase):

    def setUp(self):
        super(TestIntegration, self).setUp()
        self.folder.invokeFactory(id='mylink', type_name='Link')
        self.link = self.folder.mylink
        self.link.setRemoteUrl('http://notsupported.com/agallery')

    def testProperties(self):
        view = self.link.unrestrictedTraverse('@@gallery')
        self.failUnless(view.width == 400)
        self.portal.portal_properties.gallery_properties._updateProperty('photo_max_size', 500)

        self.failUnless(view.width == 500)

def test_suite():
    return base.build_test_suite((Test, TestIntegration))
