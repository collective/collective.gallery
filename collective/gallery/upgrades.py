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
