import doctest
import unittest2 as unittest

#from zope.testing import doctestunit
#from zope.component import testing
from Testing import ZopeTestCase as ztc
import base

def test_suite():

    TEST_CLASS = base.FunctionalTestCase
    OPTIONFLAGS = (doctest.REPORT_ONLY_FIRST_FAILURE |
                        doctest.NORMALIZE_WHITESPACE | doctest.ELLIPSIS)
    return unittest.TestSuite([

        ztc.ZopeDocFileSuite(
            'topic.txt',package='collective.gallery',
            test_class=TEST_CLASS,
            optionflags=OPTIONFLAGS
            ),

        ztc.FunctionalDocFileSuite(
            'folder.txt', package='collective.gallery',
            test_class=TEST_CLASS,
            optionflags=OPTIONFLAGS),

        ztc.FunctionalDocFileSuite(
            'link/link.txt', package='collective.gallery',
            test_class=TEST_CLASS,
            optionflags=OPTIONFLAGS),

        ])
