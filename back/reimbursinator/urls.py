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
]