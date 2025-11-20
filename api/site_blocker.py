"""
Middleware to block all access to the website and redirect to 404 page.
"""
from django.http import HttpResponseNotFound
from django.template.loader import render_to_string
from django.conf import settings

class SiteBlockerMiddleware:
    """
    Middleware that blocks all access to the website and shows 404 page.
    Works for both aktiportal.vercel.app and aktipos.vercel.app domains.
    """
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        host = (request.get_host() or '').split(':')[0]
        path = request.path or '/'
        
        # Allow static files and media to load so 404 page displays correctly
        # Also allow favicon and other common static requests
        static_paths = ['/static/', '/media/', '/favicon.ico', '/robots.txt']
        is_static = any(path.startswith(static_path) for static_path in static_paths)
        
        # Block access for both portal and example domains
        blocked_hosts = getattr(settings, 'BLOCKED_HOSTS', [])
        
        # Default blocked hosts if not set
        if not blocked_hosts:
            blocked_hosts = getattr(settings, 'PORTAL_HOSTS', []) + getattr(settings, 'EXAMPLE_HOSTS', [])
        
        # Allow localhost for development
        LOCAL_HOSTS = {"localhost", "127.0.0.1"}
        
        # Block all requests to these domains (except static files)
        if host in blocked_hosts and host not in LOCAL_HOSTS and not is_static:
            # Render the 404 template
            html = render_to_string('404.html', {
                'request': request,
            })
            return HttpResponseNotFound(html)
        
        return self.get_response(request)

