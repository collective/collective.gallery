from collective.gallery.tests import base
from collective.gallery.tests import utils

class Test(base.UnitTestCase):

    def setUp(self):
        super(Test, self).setUp()
        from collective.gallery import topic
        self.view = topic.BaseTopicView(self.context, self.request)
        self.view.settings = utils.FakeProperty
        self.view._brainToPhoto = utils.brainToPhoto

    def testPhotos(self):
        self.assertEqual(len(self.view.photos()), 2)

class TestIntegration(base.TestCase):
    pass


def test_suite():
    """This sets up a test suite that actually runs the tests in the class
    above
    """
    return base.build_test_suite((Test, TestIntegration))
