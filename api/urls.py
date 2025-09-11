"""api URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', include('other_app.urls'))
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.shortcuts import redirect
from django.contrib.auth import logout

def root_redirect(request):
    user = getattr(request, 'user', None)
    if user and user.is_authenticated:
        # If trainer-only account lands on example root, log out and send to example login
        if hasattr(user, 'trainer_profile') and not (user.is_staff or hasattr(user, 'csr_profile')):
            logout(request)
            return redirect('login')
        if user.is_staff or hasattr(user, 'csr_profile'):
            return redirect('admin_dashboard')  # example app admin dashboard
        if hasattr(user, 'trainer_profile'):
            return redirect('portal:trainer_dashboard')
    return redirect('login')

urlpatterns = [
    path('', root_redirect, name='root'),
    path('admin/', admin.site.urls),
    path('management/', include('portal.urls')),
    path('', include('example.urls')),
]
