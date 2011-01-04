import unittest

#from zope.testing import doctestunit
#from zope.component import testing
from Testing import ZopeTestCase as ztc
import base

def test_suite():
    return unittest.TestSuite([

        # Unit tests
        #doctestunit.DocFileSuite(
        #    'README.txt', package='collective.mytest',
        #    setUp=testing.setUp, tearDown=testing.tearDown),

        #doctestunit.DocTestSuite(
        #    module='collective.mytest.mymodule',
        #    setUp=testing.setUp, tearDown=testing.tearDown),


        # Integration tests that use PloneTestCase
        #ztc.ZopeDocFileSuite(
        #    'README.txt', package='collective.mytest',
        #    test_class=TestCase),

        ztc.FunctionalDocFileSuite(
            'topic.txt', package='collective.gallery',
            test_class=base.TestCase),

        ])

#    TEST_CLASS = base.FunctionalTestCase
    OPTIONFLAGS = (doctest.REPORT_ONLY_FIRST_FAILURE | 
                        doctest.NORMALIZE_WHITESPACE | doctest.ELLIPSIS)
    return unittest.TestSuite([

#        ztc.ZopeDocFileSuite(
#            'topic.txt',#package='collective.gallery',
#            test_class=TEST_CLASS,
#            #optionflags=OPTIONFLAGS
#            ),

#        ztc.FunctionalDocFileSuite(
#            'folder.txt', package='collective.gallery',
#            test_class=TEST_CLASS,
#            optionflags=OPTIONFLAGS),
#
#        ztc.FunctionalDocFileSuite(
#            'link/link.txt', package='collective.gallery',
#            test_class=TEST_CLASS,
#            optionflags=OPTIONFLAGS),

        ])
