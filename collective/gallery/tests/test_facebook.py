URL1 = "http://www.facebook.com/media/set/?set=a.416328449800.177781.275081154800"
URL2 = "http://www.facebook.com/album.php?aid=177781&id=275081154800" #put a url that is supposed to work
from collective.gallery.tests import base
from collective.gallery.tests import utils

class Test(base.UnitTestCase):

    def setUp(self):
        super(Test, self).setUp()
        self.adapter = self.getAdapter(URL1)

    def getAdapter(self, url):
        from collective.gallery.link import facebook
        self.context.remoteUrl = url
        adapter = facebook.Link(self.context)
        adapter.settings = utils.FakeProperty
        return adapter

    def testDefaultWithHeight(self):
        #test default values
        self.assertTrue(self.adapter.width == 400)
        self.assertTrue(self.adapter.height == 400)

    def testValidate(self):
        from collective.gallery.link import facebook
        self.assertTrue(facebook.check(URL1))
        self.assertFalse(facebook.check("http://no.facebook.com"))

    def testCreator(self):
        pass #not arelady supported

    def testPhotos(self):
        imgs = self.adapter.photos()
        for img in imgs:
            test, msg = utils.verifyImage(img)
            self.assertTrue(test, msg)
        self.assertTrue(len(imgs)==50, len(imgs))

    def testNotValideURL(self):
        url = 'http://www.facebook.com/album.php?aid=WRONG&id=WRONG'
        adapter = self.getAdapter(url)
        msg = "API not respected"
        self.assertTrue(adapter.creator == adapter.context.Creators()[0], msg)
        self.assertTrue(adapter.title == adapter.context.Title(), msg)
        self.assertTrue(len(adapter.photos())==0, msg)
        self.assertTrue(type(adapter.photos()) == list, msg)

class TestIntegration(base.TestCase):
    pass

