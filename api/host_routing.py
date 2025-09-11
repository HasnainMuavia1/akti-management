from django.http import HttpResponseRedirect
from django.conf import settings

LOCAL_HOSTS = {"localhost", "127.0.0.1"}

class HostRoutingMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Do nothing when DEBUG is True to avoid dev loops
        if getattr(settings, 'DEBUG', False):
            return self.get_response(request)

        host = (request.get_host() or '').split(':')[0]
        path = request.path or '/'

        # Portal domains → ensure /management/ prefix
        if host in settings.PORTAL_HOSTS:
            if not path.startswith('/management/'):
                return HttpResponseRedirect('/management/')
            return self.get_response(request)

        # Example domains → keep root; if someone hits /management/, send to /
        if host in settings.EXAMPLE_HOSTS:
            if path.startswith('/management/'):
                return HttpResponseRedirect('/')
            return self.get_response(request)

        return self.get_response(request)
