from Products.CMFCore.utils import getToolByName

def install(self):
    setup_tool = getToolByName(self, 'portal_setup')
    setup_tool.runAllImportStepsFromProfile('profile-collective.gallery:default')
    return "Ran all import steps."

def uninstall(self):
    setup_tool = getToolByName(self, 'portal_setup')
    setup_tool.runAllImportStepsFromProfile('profile-collective.gallery:uninstall')
    setup_tool.setBaselineContext('profile-Products.CMFPlone:plone')
    return "Ran all uninstall steps."
