"""
reimbursinator URL Configuration
"""

# Rupika Dikkala
# January 19, 2019

from django.contrib import admin
from django.urls import path, include

# add urls to this array
urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/', include("backend.urls")),
    path('api/v1/account/', include('rest_auth.urls')),
    path('api/v1/account/register/', include('rest_auth.registration.urls')),
    path('api/v1/accounts/', include('allauth.urls')),
    path('api-auth/', include('rest_framework.urls')),
]
