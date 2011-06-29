from collective.gallery.tests import base
from collective.gallery.tests import utils

NONAUTH_URL = 'http://picasaweb.google.fr/ceronjeanpierre/PhotosTriEsDuMariage'
AUTH_URL = 'http://picasaweb.google.com/toutpt/20091116ConcertDeRammstein?authkey=Gv1sRgCN2i5uS0y5_lLQ#'
HTTPS_URL = 'https://picasaweb.google.com/fotonowiacy/NaszeOkolice'

class Test(base.UnitTestCase):

    def setUp(self):
        super(Test, self).setUp()
        self.adapter = self.getAdapter(NONAUTH_URL)

    def getAdapter(self, url):
        from collective.gallery.link import picasaweb
        self.context.remoteUrl = url
        adapter = picasaweb.Link(self.context)
        adapter.settings = utils.FakeProperty
        return adapter

    def testDefaultWithHeight(self):
        #test default values
        self.failUnless(self.adapter.width == 400)
        self.failUnless(self.adapter.height == 400)

    def testValidate(self):
        self.failUnless(self.adapter.validate())
        adapter = self.getAdapter(AUTH_URL)
        self.failUnless(adapter.validate())
        adapter = self.getAdapter("http://nopicasa.google.com")
        self.failUnless(not adapter.validate())
        adapter = self.getAdapter(HTTPS_URL)
        self.failUnless(adapter.validate())

    def testCreator(self):
        self.failUnless(self.adapter.creator == "ceronjeanpierre")

    def testAuthKey(self):
        self.failUnless(not self.adapter.authkey)
        adapter = self.getAdapter(AUTH_URL)
        self.failUnless(adapter.authkey)

    def test_imgmax(self):
        imgmax = self.adapter.imgmax(400, 300)
        self.assertEqual(imgmax, 288)


    def testPhotosNonAuth(self):
        imgs = self.adapter.photos()
        for img in imgs:
            test, msg = utils.verifyImage(img)
            self.failUnless(test, msg)

    def testPhotosAuth(self):
        adapter = self.getAdapter(AUTH_URL)
        imgs = adapter.photos()
        for img in imgs:
            test, msg = utils.verifyImage(img)
            self.failUnless(test, msg)

    def testImgsWrongURL(self):
        adapter = self.getAdapter("http://notpicasaweb.com")
        msg = "API not respected"
        self.failUnless(adapter.creator == adapter.context.Creators()[0], msg)
        self.failUnless(adapter.title == adapter.context.Title(), msg)
        self.failUnless(len(adapter.photos())==0, msg)
        self.failUnless(type(adapter.photos()) == list, msg)

class TestIntegration(base.TestCase):
    pass

def test_suite():
   return base.build_test_suite((Test, TestIntegration))
