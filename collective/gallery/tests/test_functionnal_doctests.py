import unittest
import doctest


from Testing import ZopeTestCase as ztc

from collective.gallery.tests import base

def test_suite():
    return unittest.TestSuite([

        ztc.ZopeDocFileSuite(
            'topic.txt', package='collective.gallery',
            test_class=base.GalleryFunctionalTestCase,
            optionflags=doctest.REPORT_ONLY_FIRST_FAILURE | 
                        doctest.NORMALIZE_WHITESPACE | doctest.ELLIPSIS),
        ztc.ZopeDocFileSuite(
            'folder.txt', package='collective.gallery',
            test_class=base.GalleryFunctionalTestCase,
            optionflags=doctest.REPORT_ONLY_FIRST_FAILURE | 
                        doctest.NORMALIZE_WHITESPACE | doctest.ELLIPSIS),
        ztc.ZopeDocFileSuite(
            'link/link.txt', package='collective.gallery',
            test_class=base.GalleryFunctionalTestCase,
            optionflags=doctest.REPORT_ONLY_FIRST_FAILURE | 
                        doctest.NORMALIZE_WHITESPACE | doctest.ELLIPSIS),
        ])
