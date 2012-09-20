from Products.CMFCore.utils import getToolByName
from Products.Five.browser import BrowserView
from Products.statusmessages.interfaces import IStatusMessage

PROFILE = 'profile-collective.gallery:default'


def common(context):
    context.runAllImportStepsFromProfile(PROFILE)


class ZClean(BrowserView):
    """Call this view will cleanup the Plone install by applying the profile
    zclean"""
    def __call__(self):
        setup = getToolByName(self.context, 'portal_setup')
        setup.runAllImportStepsFromProfile(PROFILE)
        status = IStatusMessage(self.request)
        status.add("profile collective.gallery:zclean applied")
        self.request.response.redirect(self.context.absolute_url())

def zclean(context):
    context.runAllImportStepsFromProfile('profile-collective.gallery:zclean')
