"""octofit_tracker URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
import os
from django.contrib import admin
from django.urls import path, include
from django.http import JsonResponse
from django.shortcuts import redirect

# DRF router will expose API endpoints under /api/
from rest_framework import routers
from .views import ActivityViewSet

# register API routes
router = routers.DefaultRouter()
router.register(r'activities', ActivityViewSet, basename='activity')


def api_root(request):
    """A small API root that builds URLs using the CODESPACE_NAME env var when available.

    This avoids relying on request.build_absolute_uri() and lets the URLs point
    to the Codespace HTTPS host (https://$CODESPACE_NAME-8000.app.github.dev).
    """
    codespace = os.environ.get('CODESPACE_NAME')
    if codespace:
        base = f"https://{codespace}-8000.app.github.dev"
    else:
        # fallback to the request host and scheme
        scheme = 'https' if request.is_secure() else 'http'
        base = f"{scheme}://{request.get_host()}"

    data = {
        'activities': f"{base}/api/activities/",
        'users': f"{base}/api/users/",
        'teams': f"{base}/api/teams/",
    }
    return JsonResponse(data)


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', lambda request: redirect('api-root')),
    path('api/', api_root, name='api-root'),
    # include DRF router endpoints under /api/
    path('api/', include(router.urls)),
]
