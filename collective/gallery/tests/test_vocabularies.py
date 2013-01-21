from zope import component
from zope.schema.interfaces import IVocabularyFactory
from collective.gallery.tests import base


class IntegrationTestVocabularies(base.TestCase):

    def test_image_scale(self):
        name = "collective.gallery.ImageScaleVocabulary"
        factory = component.queryUtility(IVocabularyFactory, name)
        vocab = factory(self.portal)
        self.assertEqual(len(vocab), 7)
        mini = vocab.getTerm('mini')
        self.assertFalse(mini.title)  # has no title ?
        self.assertEqual(mini.token, 'mini(200, 200)')
        self.assertEqual(mini.value, 'mini')
