"""
Root URL Configuration for Gentle Care Transit API
"""

from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from rest_framework import routers

urlpatterns = [
    # Admin
    path('admin/', admin.site.urls),
    
    # API v1
    path('api/v1/accounts/', include('accounts.urls')),
    path('api/v1/patients/', include('patients.urls')),
    path('api/v1/drivers/', include('drivers.urls')),
    path('api/v1/vehicles/', include('vehicles.urls')),
    path('api/v1/bookings/', include('bookings.urls')),
    path('api/v1/trips/', include('trips.urls')),
    path('api/v1/billing/', include('billing.urls')),
    path('api/v1/ratings/', include('ratings.urls')),
    path('api/v1/notifications/', include('notifications.urls')),
    path('api/v1/reports/', include('reports.urls')),
]

# Serve media files in development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
