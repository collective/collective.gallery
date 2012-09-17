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
        self.failUnless(self.adapter.width == 400)
        self.failUnless(self.adapter.height == 400)

    def testValidate(self):
        self.failUnless(self.adapter.validate())
        self.context.remoteUrl = "http://not.flickr.com"
        adapter = self.getAdapter()
        self.failUnless(not adapter.validate())

    def testExtractData(self):
        from collective.gallery.link.flickr import extract_data
        tests = [
            ('http://foo',
             [('searchtags', None), ('sets', None), ('type', None), ('yahoo_account', None),]),
            ('http://www.flickr.com/photos/princeofnorway',
             [('searchtags', None), ('sets', None), ('type', 'photos'), ('yahoo_account', 'princeofnorway')] ),
            ('http://www.flickr.com/photos/princeofnorway/sets/foo/searchtags/foo,bar',
             [('searchtags', 'foo,bar'), ('sets', 'foo'), ('type', 'photos'), ('yahoo_account', 'princeofnorway')]),
            ('http://www.flickr.com/photos/searchtags/foo,bar',
             [('searchtags', 'foo,bar'), ('sets', None), ('type', 'photos'), ('yahoo_account', None)]),
        ]
        def dotest(test, wanted):
            res = extract_data(test)
            res = res.items()
            res.sort()
            self.assertEqual(res, wanted)
        for test, wanted in tests:
            dotest(test, wanted)

    def testCreator(self):
        self.failUnless(self.adapter.creator == "CJsarp")

    def testUserInfo(self):
        user_info = self.adapter.user_info
        self.failUnless(user_info['user_id']=="41300176@N02")
        self.failUnless(user_info['username']=="CJsarp")
        self.failUnless(user_info['user_yahooaccount']=="princeofnorway")

    def testPhotos(self):
        imgs = self.adapter.photos()
        for img in imgs:
            test, msg = utils.verifyImage(img)
            self.failUnless(test, msg)

    def testPhotosUserDirect(self):
        self.context.remoteUrl = 'http://www.flickr.com/photos/kiorky/'
        adapter = self.getAdapter(self.context)
        imgs = adapter.photos()
        self.assertTrue(len(imgs)>1)

    def testPhotosSet(self):
        self.context.remoteUrl = 'http://www.flickr.com/photos/kiorky/sets/72157631537964233/'
        adapter = self.getAdapter(self.context)
        imgs = adapter.photos()
        self.assertTrue(len(imgs)==1)


    def testPhotosSearchTags(self):
        self.context.remoteUrl = 'http://www.flickr.com/photos/kiorky/searchtags/azerty'
        adapter = self.getAdapter(self.context)
        imgs = adapter.photos()
        self.assertTrue(len(imgs)==1)

    def testPhotosSearchMultTags(self):
        self.context.remoteUrl = 'http://www.flickr.com/photos/kiorky/searchtags/azerty,123'
        adapter = self.getAdapter(self.context)
        imgs = adapter.photos()
        self.assertTrue(len(imgs)==2)

    def testPhotosSearchTagsWOUser(self):
        self.context.remoteUrl = 'http://www.flickr.com/photos/searchtags/2009'
        adapter = self.getAdapter(self.context)
        imgs = adapter.photos()
        self.assertTrue(len(imgs)>10)

    def testNotValideURL(self):
        url = 'http://nota.flickr.com/url'
        self.context.remoteUrl = url
        self.context._modified = "updated 2"
        adapter = self.getAdapter()
        msg = "API not respected"
        self.failUnless(adapter.creator == adapter.context.Creators()[0], msg)
        self.failUnless(adapter.title == adapter.context.Title(), msg)
        self.failUnless(len(adapter.photos())==0, msg)
        self.failUnless(type(adapter.photos()) == list, msg)

    def testWUser(self):
        self.context.remoteUrl = 'http://www.flickr.com/photos/kiorky'
        adapter = self.getAdapter(self.context)
        user_info = adapter.user_info
        self.assertEqual(user_info['user_id'], '87215164@N02')

    def testWOUser(self):
        self.context.remoteUrl = 'http://www.flickr.com/'
        adapter = self.getAdapter(self.context)
        user_info = adapter.user_info
        self.assertEqual(user_info['user_id'], None)


    def testWOUserTags(self):
        self.context.remoteUrl = 'http://www.flickr.com/photos/searchtags/1,2,3'
        adapter = self.getAdapter(self.context)
        user_info = adapter.user_info
        self.assertEqual(user_info['user_id'], None)

class TestIntegration(base.TestCase):
    pass

def test_suite():
    return base.build_test_suite((Test, TestIntegration))
