from Products.CMFCore.utils import getToolByName

def upgrade_to_10(context):
    context.runAllImportStepsFromProfile('profile-collective.gallery:default')
    catalog = getToolByName(context, 'portal_catalog')

    def update_layout(brain):
        ob = brain.getObject()
        #TODO: update layout to gallery.html

    def update_layouts(portal_type):
        brains = catalog(portal_type=portal_type)
        map(update_layout, brains)

    for portal_type in ('Link', 'Folder', 'Topic'):
        update_layouts(portal_type)

