from collective.gallery.tests import base
from collective.gallery.tests import utils


class UnitTestLink(base.UnitTestCase):

    def setUp(self):
        super(UnitTestLink, self).setUp()
        from collective.gallery import link
        self.view = link.BaseLinkView(self.context, self.request)
        self.view.settings = utils.FakeProperty

    def testPhotos(self):
        imgs = self.view.photos()
        self.assertTrue(not imgs)
        self.assertTrue(len(imgs) == 0)

    def testCreator(self):
        self.assertTrue(self.view.creator == self.view.context.Creators()[0])


class IntegrationTestLink(base.TestCase):

    def setUp(self):
        super(IntegrationTestLink, self).setUp()
        self.folder.invokeFactory(id='mylink', type_name='Link')
        self.link = self.folder.mylink
        self.link.setRemoteUrl('http://notsupported.com/agallery')
        self.view = self.link.unrestrictedTraverse('@@gallery')

    def testRegistry(self):
        self.assertTrue(self.view.width == 400)
        key = 'collective.gallery.interfaces.IGallerySettings.photo_max_size'
        self.portal.portal_registry[key] = 500

        self.assertTrue(self.view.width == 500)

    def test_update(self):
        from collective.gallery.link.picasaweb import Link
        url = 'https://picasaweb.google.com/nantesmetropoledeveloppement/'
        url += 'DiaporamaCoeurDeNantes'
        self.view.url = url
        self.view.update()
        self.assertIsNotNone(self.view.resource)
        self.assertIsInstance(self.view.resource, Link)
