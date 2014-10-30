from django.utils import simplejson
from django.http import HttpResponse


class JsonResponse(HttpResponse):
    """Return a Json Format."""
    def __init__(self, data):
        HttpResponse.__init__(self,
                              content=simplejson.dumps(data),
                              content_type='application/json')
