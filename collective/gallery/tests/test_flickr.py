from collective.gallery.tests import base
from collective.gallery.tests import utils

URL_SETS_PUBLIC = 'http://www.flickr.com/photos/princeofnorway/sets/'
URL_SETS_PUBLIC += '72157622650234713/'


class UnitTestFlickr(base.UnitTestCase):

    def setUp(self):
        super(UnitTestFlickr, self).setUp()
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
        self.assertEqual(self.adapter.width, 400)
        self.assertEqual(self.adapter.height, 400)

    def testValidate(self):
        from collective.gallery.link import flickr
        self.assertTrue(flickr.check(URL_SETS_PUBLIC))
        self.assertFalse(flickr.check("http://not.flickr.com"))

    def testExtractData(self):
        from collective.gallery.link.flickr import extract_data
        tests = [
            ('http://foo',
             [('searchtags', None), ('sets', None), ('type', None),
              ('yahoo_account', None)]),
            ('http://www.flickr.com/photos/princeofnorway',
             [('searchtags', None), ('sets', None), ('type', 'photos'),
              ('yahoo_account', 'princeofnorway')]),
            ('http://www.flickr.com/photos/princeofnorway/sets/foo/\
                  searchtags/foo,bar'.replace(' ', ''),
             [('searchtags', 'foo,bar'), ('sets', 'foo'), ('type', 'photos'),
              ('yahoo_account', 'princeofnorway')]),
            ('http://www.flickr.com/photos/searchtags/foo,bar',
             [('searchtags', 'foo,bar'), ('sets', None), ('type', 'photos'),
              ('yahoo_account', None)]),
            ('http://www.flickr.com/photos/yahoo_account/foo/sets',
             [('searchtags', None), ('sets', None), ('type', 'photos'),
              ('yahoo_account', 'yahoo_account')]),
            ('http://www.flickr.com/photos/yahoo_account/foo/sets/\
              searchtags/foo'.replace(' ', ''),
             [('searchtags', 'foo'), ('sets', None), ('type', 'photos'),
              ('yahoo_account', 'yahoo_account')]),
        ]

        def dotest(test, wanted):
            res = extract_data(test)
            res = res.items()
            res.sort()
            self.assertEqual(res, wanted, msg="fails on %s" % test)

        for test, wanted in tests:
            dotest(test, wanted)

    def testCreator(self):
        self.assertEqual(self.adapter.creator, "CJsarp")

    def testUserInfo(self):
        user_info = self.adapter.user_info
        self.assertEqual(user_info['user_id'], "41300176@N02")
        self.assertEqual(user_info['username'], "CJsarp")
        self.assertEqual(user_info['user_yahooaccount'], "princeofnorway")

    def testNotExistingUserExtracted(self):
        self.context.remoteUrl = 'http://www.flickr.com/photos/\
            notexistinguser/sets'
        adapter = self.getAdapter(self.context)
        with self.assertRaises(Exception):
            adapter.user_info

    def testPhotos(self):
        imgs = self.adapter.photos()
        for img in imgs:
            test, msg = utils.verifyImage(img)
            self.assertTrue(test, msg)

    def testPhotosUserDirect(self):
        self.context.remoteUrl = 'http://www.flickr.com/photos/kiorky/'
        adapter = self.getAdapter(self.context)
        imgs = adapter.photos()
        self.assertTrue(len(imgs) > 1)

    def testPhotosSet(self):
        self.context.remoteUrl = 'http://www.flickr.com/photos/kiorky/sets/\
            72157631537964233/'.replace(' ', '')
        adapter = self.getAdapter(self.context)
        imgs = adapter.photos()
        self.assertEqual(len(imgs), 1)

    def testPhotosSearchTags(self):
        self.context.remoteUrl = 'http://www.flickr.com/photos/kiorky/\
            searchtags/azerty'.replace(' ', '')
        adapter = self.getAdapter(self.context)
        imgs = adapter.photos()
        self.assertEqual(len(imgs), 1)

    def testPhotosSearchMultTags(self):
        self.context.remoteUrl = 'http://www.flickr.com/photos/kiorky/\
            searchtags/azerty,123'.replace(' ', '')
        adapter = self.getAdapter(self.context)
        imgs = adapter.photos()
        self.assertEqual(len(imgs), 2)

    def testPhotosSearchTagsWOUser(self):
        self.context.remoteUrl = 'http://www.flickr.com/photos/searchtags/2009'
        adapter = self.getAdapter(self.context)
        imgs = adapter.photos()
        self.assertTrue(len(imgs) > 10)

    def testNotValideURL(self):
        url = 'http://nota.flickr.com/url'
        self.context.remoteUrl = url
        self.context._modified = "updated 2"
        adapter = self.getAdapter()
        msg = "API not respected"
        self.assertEqual(adapter.title, adapter.context.Title(), msg)
        self.assertEqual(len(adapter.photos()), 0, msg)
        self.assertEqual(type(adapter.photos()), list, msg)

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
        self.context.remoteUrl = 'http://www.flickr.com/photos/\
            searchtags/1,2,3'.replace(' ', '')
        adapter = self.getAdapter(self.context)
        user_info = adapter.user_info
        self.assertEqual(user_info['user_id'], None)


class TestIntegration(base.TestCase):
    pass
