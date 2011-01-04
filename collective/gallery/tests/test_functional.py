import unittest
import doctest


from Testing import ZopeTestCase as ztc

from collective.gallery.tests import base

def test_suite():
    TEST_CLASS = base.FunctionalTestCase
    OPTIONFLAGS = (doctest.REPORT_ONLY_FIRST_FAILURE | 
                        doctest.NORMALIZE_WHITESPACE | doctest.ELLIPSIS)
    return unittest.TestSuite([

        ztc.FunctionalDocFileSuite(
            'topic.txt', package='collective.gallery',
            test_class=TEST_CLASS,
            optionflags=OPTIONFLAGS),

        ztc.FunctionalDocFileSuite(
            'folder.txt', package='collective.gallery',
            test_class=TEST_CLASS,
            optionflags=OPTIONFLAGS),

        ztc.FunctionalDocFileSuite(
            'link/link.txt', package='collective.gallery',
            test_class=TEST_CLASS,
            optionflags=OPTIONFLAGS),

        ])