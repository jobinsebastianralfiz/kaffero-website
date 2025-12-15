"""
URL configuration for Kaffero showcase website.
"""

from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path

from website.admin import kaffero_admin

urlpatterns = [
    path('admin/', kaffero_admin.urls),  # Django admin (backup)
    path('dashboard/', include('website.dashboard_urls', namespace='dashboard')),  # Custom dashboard
    path('', include('website.urls')),
]

# Serve media files in development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATICFILES_DIRS[0])
