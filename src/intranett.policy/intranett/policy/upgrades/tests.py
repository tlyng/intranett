import os

from plone.app.testing import TEST_USER_ID
from Products.CMFCore.utils import getToolByName

from intranett.policy.upgrades import steps
from intranett.policy.tests.base import IntranettTestCase


class TestUpgradeSteps(IntranettTestCase):

    def test_activate_clamav(self):
        portal = self.layer['portal']
        ptool = getToolByName(portal, 'portal_properties')
        clamav = ptool.clamav_properties
        clamav._updateProperty('clamav_connection', 'net')
        steps.activate_clamav(portal)
        self.assertEqual(clamav.getProperty('clamav_connection'), 'socket')
        self.assertEqual(
            clamav.getProperty('clamav_socket'), '/var/run/clamav/clamd.sock')

    def test_disable_folderish_sections(self):
        portal = self.layer['portal']
        ptool = getToolByName(portal, 'portal_properties')
        site_properties = ptool.site_properties
        site_properties.disable_nonfolderish_sections = False
        steps.disable_nonfolderish_sections(portal)
        self.assertTrue(
            site_properties.getProperty('disable_nonfolderish_sections'))

    def test_activate_collective_flag(self):
        portal = self.layer['portal']
        catalog = getToolByName(portal, 'portal_catalog')
        catalog.delIndex('flaggedobject')
        steps.activate_collective_flag(portal)
        self.assertTrue('flaggedobject' in catalog.indexes())

    def test_activate_iw_rejectanonymous(self):
        from iw.rejectanonymous import IPrivateSite
        from zope.interface import noLongerProvides
        portal = self.layer['portal']
        setup = getToolByName(portal, 'portal_setup')
        noLongerProvides(portal, IPrivateSite)
        self.assertFalse(IPrivateSite.providedBy(portal))
        steps.setup_reject_anonymous(setup)
        self.assertTrue(IPrivateSite.providedBy(portal))

    def test_install_memberdata_type(self):
        portal = self.layer['portal']
        types = getToolByName(portal, 'portal_types')
        del types['MemberData']
        steps.install_memberdata_type(portal)
        self.assertTrue('MemberData' in types)

    def test_update_caching_config(self):
        portal = self.layer['portal']
        registry = getToolByName(portal, 'portal_registry')
        purge_key = 'plone.app.caching.interfaces.IPloneCacheSettings.' \
            'purgedContentTypes'
        etag_key = 'plone.app.caching.weakCaching.etags'
        registry.records[purge_key].value = ('Document', )
        registry.records[etag_key].value = ('userid', 'language', )
        steps.update_caching_config(portal)
        self.assertEqual(registry.records[purge_key].value,
            ('File', 'Image', 'News Item'))
        self.assertTrue('editbar' in registry.records[etag_key].value)

    def test_migrate_portraits(self):
        from OFS.Image import Image
        from intranett.policy.tests.test_userdata import TEST_IMAGES
        from intranett.policy.tests.utils import make_file_upload
        from intranett.policy.tools import Portrait

        portal = self.layer['portal']

        mdt = getToolByName(portal, 'portal_memberdata')
        path = os.path.join(TEST_IMAGES, 'test.jpg')
        image_jpg = make_file_upload(path, 'image/jpeg', 'myportrait.jpg')

        image = Image(id=TEST_USER_ID, file=image_jpg, title='')
        thumb = Image(id=TEST_USER_ID, file=image_jpg, title='')
        mdt._setPortrait(image, TEST_USER_ID)
        mdt._setPortrait(thumb, TEST_USER_ID, thumbnail=True)

        steps.migrate_portraits(portal)

        self.assertTrue(TEST_USER_ID in mdt.portraits)
        self.assertTrue(TEST_USER_ID in mdt.thumbnails)
        self.assertTrue(isinstance(mdt.portraits[TEST_USER_ID], Portrait))
        self.assertTrue(isinstance(mdt.thumbnails[TEST_USER_ID], Portrait))

    def test_disable_webstats_js(self):
        portal = self.layer['portal']
        ptool = getToolByName(portal, 'portal_properties')
        sprops = ptool.site_properties
        sprops.webstats_js = '<script type="text/javascript" />'
        steps.disable_webstats_js(portal)
        self.assertEqual(sprops.webstats_js, '')