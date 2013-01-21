from collective.gallery.tests import base


class UnitTestCore(base.UnitTestCase):

    def setUp(self):
        super(UnitTestCore, self).setUp()
        from collective.gallery import core
        self.view = core.BaseBrowserView(self.context, self.request)

    def test_title(self):
        self.assertEqual(self.view.title, "a title")

    def test_creator(self):
        self.assertEqual(self.view.creator, "myself")

    def test_description(self):
        self.assertEqual(self.view.description, "a description")

    def test_date(self):
        self.assertEqual(self.view.date, "a date")

    def test_photos(self):
        self.assertTrue(not self.view.photos())
        self.assertEqual(type(self.view.photos()), list)

    def test_get_photo(self):
        photo = self.view.get_photo()
        self.assertIsInstance(photo, dict)
        self.assertIn('url', photo)
        self.assertIn('title', photo)
        self.assertIn('description', photo)
        self.assertIn('thumb_url', photo)


class TestIntegrationCore(base.TestCase):
    def setUp(self):
        super(TestIntegrationCore, self).setUp()
        from collective.gallery import core
        self.view = core.BaseBrowserView(self.portal, None)
        self.registry = self.portal.portal_registry

    def test_registry(self):
        self.assertEqual(self.view.width, 400)
        key = 'collective.gallery.interfaces.IGallerySettings.photo_max_size'
        self.registry[key] = 500
        self.assertEqual(self.view.width, 500)

    def test_width(self):
        self.assertEqual(self.view.width, 400)

    def test_heigth(self):
        self.assertEqual(self.view.width, 400)
