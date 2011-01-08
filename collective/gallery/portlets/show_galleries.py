# -*- coding: utf-8 -*-
#
# GNU General Public License (GPL)
#
__author__ = """Johannes Raggam <johannes@raggam.co.at>"""
__docformat__ = 'plaintext'

from zope import schema
from zope.formlib import form
from zope.interface import implements
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from plone.portlets.interfaces import IPortletDataProvider
from plone.app.portlets.portlets import base

from Acquisition import aq_inner
from Products.CMFCore.utils import getToolByName

from collective.gallery import messageFactory as _

import random
from Products.ATContentTypes.interfaces import IATImage

class IShowGalleriesPortlet(IPortletDataProvider):
    search_portal = schema.Bool(
        title=u'Search portal for galleries',
        description=u'If selected, search the whole portal for galleries.'\
            'otherwise search only subfolders of the current path.',
        required=True,
        default=True)

    num_pictures = schema.Int(
        title=u'Number of Pictures',
        description=u'Define the number of pictures to show in the portlet',
        required=True,
        default=1,
        min=1)


class Assignment(base.Assignment):
    implements(IShowGalleriesPortlet)

    def __init__(self, search_portal=True, num_pictures=1):
        self.search_portal= search_portal
        self.num_pictures = num_pictures

    @property
    def title(self):
        return _(u"Show Galleries Portlet")


class AddForm(base.AddForm):
    form_fields = form.Fields(IShowGalleriesPortlet)
    label = _(u"Add portlet to show the pictures of the portals galleries")
    description = _(u"This portlet shows the pictures of the portals galleries.")

    def create(self, data):
        return Assignment(**data)


class EditForm(base.EditForm):
    form_fields = form.Fields(IShowGalleriesPortlet)
    label = _(u"Add portlet to show the pictures of the portals galleries")
    description = _(u"This portlet shows the pictures of the portals galleries.")


class Renderer(base.Renderer):
    render = ViewPageTemplateFile('show_galleries.pt')

    # TODO: cache me
    def get_galleries(self):
        context = aq_inner(self.context)
        if self.data.search_portal:
            portal_url = getToolByName(context, 'portal_url')
            context = portal_url.getPortalObject()
        cat = getToolByName(context,'portal_catalog')

        query = {}
        query['is_folderish'] = True
        query['path'] = {'query': '/'.join(context.getPhysicalPath())}
        brains = cat(**query)

        # TODO: import gallery view names from config.py or make this somehow
        #       more generic
        return [brain for brain in brains
                if brain.getObject().defaultView() in ('gallery.html',)]

    def get_gallery_pictures(self):
        num_pictures = self.data.num_pictures
        galleries = self.get_galleries()
        if not galleries: return []
        gallery = random.choice(galleries).getObject()
        pictures = [pic for pic in gallery.contentValues()
                    if IATImage.providedBy(pic)]
        if len(pictures) > num_pictures:
            pictures = random.sample(pictures, num_pictures)
        return {'gallery': gallery, 'pictures': pictures}

    @property
    def available(self):
        # TODO: if not search_portal, only show me for folderish contexts
        return True

