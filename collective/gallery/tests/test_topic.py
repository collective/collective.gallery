import unittest
from collective.gallery.tests import utils
from zope.publisher.browser import TestRequest as Request

class Test(unittest.TestCase):
    
    def setUp(self):
        from collective.gallery import topic
        self.context = utils.FakeTopic()
        self.request = Request()
        utils.make_request_annotable(self.request)
        self.view = topic.BaseTopicView(self.context, self.request)
        self.view.settings = utils.FakeProperty
        self.view._brainToPhoto = utils.brainToPhoto

    def testPhotos(self):
        self.assertEqual(len(self.view.photos()), 2)

def test_suite():
    """This sets up a test suite that actually runs the tests in the class
    above
    """
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(Test))
    return suite
