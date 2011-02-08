from Products.Five import BrowserView

class Gallery(BrowserView):
    """gallery view"""

    def __init__(self, context, request):
        self.context = context
        self.request = request
