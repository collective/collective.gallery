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
        self.assertTrue(not imgs)
        self.assertTrue(len(imgs) == 0)

    def testCreator(self):
        self.assertTrue(self.view.creator == self.view.context.Creators()[0])

class TestIntegration(base.TestCase):

    def setUp(self):
        super(TestIntegration, self).setUp()
        self.folder.invokeFactory(id='mylink', type_name='Link')
        self.link = self.folder.mylink
        self.link.setRemoteUrl('http://notsupported.com/agallery')

    def testRegistry(self):
        view = self.link.unrestrictedTraverse('@@gallery')
        self.assertTrue(view.width == 400)
        key = 'collective.gallery.interfaces.IGallerySettings.photo_max_size'
        self.portal.portal_registry[key] = 500

        self.assertTrue(view.width == 500)

