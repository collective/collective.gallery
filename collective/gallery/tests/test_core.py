import unittest

class Test(unittest.TestCase):
    
    def setUp(self):
        from collective.gallery import core
        from collective.gallery.tests import utils
        from ZPublisher.tests.testPublish import Request

        self.context = utils.FakeContext()
        self.request = Request()
        self.view = core.BaseBrowserView(self.context, self.request)

    def testTitle(self):
        self.assertEqual(self.view.title, "a title")

    def testCreator(self):
        self.assertEqual(self.view.creator, "myself")

    def testDescription(self):
        self.assertEqual(self.view.description, "a description")

    def testDate(self):
        self.assertEqual(self.view.date, "a date")

    def testPhotos(self):
        self.failUnless(not self.view.photos())
        self.assertEqual(type(self.view.photos()), list)

    def testSize(self):
        from collective.gallery import core
        available_sizes = [('400','400'),('300','300'),('200','200')]
        asked_size = ('350','350')
        w,h = core.sizes(available_sizes, asked_size)
        self.failUnless(w=='300', w)
        self.failUnless(h=='300', h)

def test_suite():
    """This sets up a test suite that actually runs the tests in the class
    above
    """
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(Test))
    return suite
