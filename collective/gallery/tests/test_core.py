from collective.gallery.tests import base

class Test(base.UnitTestCase):
    
    def setUp(self):
        super(Test, self).setUp()
        from collective.gallery import core
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
        self.assertTrue(not self.view.photos())
        self.assertEqual(type(self.view.photos()), list)

class TestIntegration(base.TestCase):
    
    def testRegistry(self):
        from collective.gallery import core
        from plone.registry.interfaces import IRegistry
        view = core.BaseBrowserView(self.portal, None)
        registry = self.portal.portal_registry
        self.assertTrue(view.width == 400)
        key = 'collective.gallery.interfaces.IGallerySettings.photo_max_size'
        registry[key] = 500
        self.assertTrue(view.width == 500)

