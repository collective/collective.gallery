import logging
from zope.i18nmessageid import MessageFactory

messageFactory = MessageFactory("collective.gallery")
logger = logging.getLogger('collective.gallery')

def initialize(context):
    """initialize"""
