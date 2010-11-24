import doctest
from unittest import TestSuite

from Testing.ZopeTestCase import ZopeDocFileSuite

from intranett.policy.tests.base import IntranettFunctionalTestCase

optionflags = (doctest.ELLIPSIS | doctest.NORMALIZE_WHITESPACE)


def test_suite():
    suite = TestSuite([
        ZopeDocFileSuite(
            'comments.txt', package='intranett.theme.tests',
            test_class=IntranettFunctionalTestCase,
            optionflags=optionflags),
        ZopeDocFileSuite(
            'employeelisting.txt', package='intranett.theme.tests',
            test_class=IntranettFunctionalTestCase,
            optionflags=optionflags),
        ZopeDocFileSuite(
            'frontpage.txt', package='intranett.theme.tests',
            test_class=IntranettFunctionalTestCase,
            optionflags=optionflags),
        ZopeDocFileSuite(
            'robots.txt', package='intranett.theme.tests',
            test_class=IntranettFunctionalTestCase,
            optionflags=optionflags),
        ])
    return suite