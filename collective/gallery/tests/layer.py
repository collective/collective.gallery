from plone.testing import z2

from plone.app.testing import PloneSandboxLayer
from plone.app.testing import PLONE_FIXTURE
from plone.app.testing import IntegrationTesting, FunctionalTesting

class CollectiveGalleryLayer(PloneSandboxLayer):
    default_bases = (PLONE_FIXTURE,)

    def setUpZope(self, app, configurationContext):
        # Load ZCML
        import collective.gallery
        import collective.js.galleriffic
        self.loadZCML(package=collective.gallery)
        self.loadZCML(package=collective.js.galleriffic)

        # Install product and call its initialize() function
        z2.installProduct(app, 'collective.gallery')
        z2.installProduct(app, 'collective.js.galleriffic')

    def setUpPloneSite(self, portal):
        # Install into Plone site using portal_setup
        self.applyProfile(portal, 'collective.gallery:default')

    def tearDownZope(self, app):
        # Uninstall product
        z2.uninstallProduct(app, 'collective.gallery')
        z2.uninstallProduct(app, 'collective.js.galleriffic')

FIXTURE = CollectiveGalleryLayer()

GALLERY_INTEGRATION = IntegrationTesting(bases=(FIXTURE,), name="Gallery:Integration")
GALLERY_FUNCTIONAL = FunctionalTesting(bases=(FIXTURE,), name="Gallery:Functional")
