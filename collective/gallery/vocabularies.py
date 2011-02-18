from zope.interface import directlyProvides
from zope.schema.interfaces import IVocabularyFactory
from zope.schema.vocabulary import SimpleVocabulary
try:
    from plone.app.imaging.utils import getAllowedSizes
except ImportError, e:
    #plone3 bbb
    def getAllowedSizes():
        return {'large'   : (768, 768),
               'preview' : (400, 400),
               'mini'    : (200, 200),
               'thumb'   : (128, 128),
               'tile'    :  (64, 64),
               'icon'    :  (32, 32),
               'listing' :  (16, 16),
              }

def ImageScaleVocabulary(context):
    allowed_sizes = getAllowedSizes()
    items = [("%s(%s, %s)" %(key, value[0], value[1]), key)
        for key,value in allowed_sizes.items() if allowed_sizes]
    return SimpleVocabulary.fromItems(items)
directlyProvides(ImageScaleVocabulary, IVocabularyFactory)
