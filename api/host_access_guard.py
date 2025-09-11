from django.conf import settings
from django.shortcuts import redirect
from django.contrib.auth import logout

LOCAL_HOSTS = {"localhost", "127.0.0.1"}

class HostAccessGuardMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        host = (request.get_host() or '').split(':')[0]
        # Only enforce on production/example hosts; skip localhost for dev convenience
        if host in getattr(settings, 'EXAMPLE_HOSTS', []) and host not in LOCAL_HOSTS:
            user = getattr(request, 'user', None)
            if user and user.is_authenticated:
                # If the user is a trainer (portal-only) and not staff/CSR, log them out here
                is_trainer = hasattr(user, 'trainer_profile')
                is_staff_or_csr = user.is_staff or hasattr(user, 'csr_profile')
                if is_trainer and not is_staff_or_csr:
                    logout(request)
                    return redirect('login')  # example app login
        return self.get_response(request)
