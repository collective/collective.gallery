from collective.gallery.tests import base
from collective.gallery.tests import utils

URL_SETS_PUBLIC = 'http://www.flickr.com/photos/princeofnorway/sets/72157622650234713/'

class Test(base.UnitTestCase):

    def setUp(self):
        super(Test, self).setUp()
        self.context.remoteUrl = URL_SETS_PUBLIC
        self.adapter = self.getAdapter()

    def getAdapter(self, link=None):
        if not link:
            link = self.context
        from collective.gallery.link import flickr
        adapter = flickr.Link(link)
        adapter.settings = utils.FakeProperty
        return adapter

    def testDefaultWithHeight(self):
        self.assertTrue(self.adapter.width == 400)
        self.assertTrue(self.adapter.height == 400)

    def testValidate(self):
        from collective.gallery.link import flickr
        self.assertTrue(flickr.check(URL_SETS_PUBLIC))
        self.assertFalse(flickr.check("http://not.flickr.com"))

    def testCreator(self):
        self.assertTrue(self.adapter.creator == "CJsarp")

    def testUserInfo(self):
        user_info = self.adapter.user_info
        self.assertTrue(user_info['user_id']=="41300176@N02")
        self.assertTrue(user_info['username']=="CJsarp")
        self.assertTrue(user_info['user_yahooaccount']=="princeofnorway")

    def testPhotos(self):
        imgs = self.adapter.photos()
        for img in imgs:
            test, msg = utils.verifyImage(img)
            self.assertTrue(test, msg)

    def testNotValideURL(self):
        url = 'http://nota.flickr.com/url'
        self.context.remoteUrl = url
        self.context._modified = "updated 2"
        adapter = self.getAdapter()
        msg = "API not respected"
        self.assertTrue(adapter.title == adapter.context.Title(), msg)
        self.assertTrue(len(adapter.photos())==0, msg)
        self.assertTrue(type(adapter.photos()) == list, msg)

class TestIntegration(base.TestCase):
    pass
