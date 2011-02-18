from Products.CMFCore.utils import getToolByName

def upgrade_1_to_10(context):
    context.runAllImportStepsFromProfile('profile-collective.gallery:default')
    catalog = getToolByName(context, 'portal_catalog')

    def update_layout(brain):
        ob = brain.getObject()
        if ob.getProperty('layout') in ('galleriffic', 'gallery', '@@gallery',
                                        's3slider', 'dewslider'):
            ob._updateProperty('layout', 'gallery.html')

    def update_layouts(portal_type):
        brains = catalog(portal_type=portal_type)
        map(update_layout, brains)

    for portal_type in ('Link', 'Folder', 'Topic'):
        update_layouts(portal_type)

def upgrade_10_to_11(context):
    """Some properties has been removed. a browserlayer has been added
    """
    context.runAllImportStepsFromProfile('profile-collective.gallery:default')

def upgrade_11_to_12(context):
    """Portlet has been added.
    """
    context.runImportStepFromProfile('profile-collective.gallery:default', 'portlets')

def upgrade_12_to_13(context):
    """Add a dependency on collective.portlet.itemview
    """
    context.runImportStepFromProfile('profile-collective.gallery:default', 'jsregistry')

def upgrade_13_to_14(context):
    """Update gallery portlet with image_size field.
    """
    pass
