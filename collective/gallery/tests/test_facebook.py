from collective.gallery.tests import base
from collective.gallery.tests import utils

URL1 = "http://www.facebook.com/media/set/"
URL1 += "?set=a.416328449800.177781.275081154800"
URL2 = "http://www.facebook.com/album.php?aid=177781&id=275081154800"


class UnitTestFacebook(base.UnitTestCase):

    def setUp(self):
        super(UnitTestFacebook, self).setUp()
        self.adapter = self.getAdapter(URL1)

    def getAdapter(self, url):
        from collective.gallery.link import facebook
        self.context.remoteUrl = url
        adapter = facebook.Link(self.context)
        adapter.settings = utils.FakeProperty
        return adapter

    def testDefaultWithHeight(self):
        #test default values
        self.assertEqual(self.adapter.width, 400)
        self.assertEqual(self.adapter.height, 400)

    def testValidate(self):
        from collective.gallery.link import facebook
        self.assertTrue(facebook.check(URL1))
        self.assertFalse(facebook.check("http://no.facebook.com"))

    def testCreator(self):
        pass  # not arelady supported

    def testPhotos(self):
        imgs = self.adapter.photos()
        for img in imgs:
            test, msg = utils.verifyImage(img)
            self.assertTrue(test, msg)
        self.assertEqual(len(imgs), 50, len(imgs))

    def testNotValideURL(self):
        url = 'http://www.facebook.com/album.php?aid=WRONG&id=WRONG'
        adapter = self.getAdapter(url)
        msg = "API not respected"
        self.assertEqual(adapter.creator, adapter.context.Creators()[0], msg)
        self.assertEqual(adapter.title, adapter.context.Title(), msg)
        self.assertEqual(len(adapter.photos()), 0, msg)
        self.assertEqual(type(adapter.photos()), list, msg)


class TestIntegration(base.TestCase):
    pass
