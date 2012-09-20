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

