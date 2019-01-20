# Rupika Dikkala
# January 19, 2019
# Add views for each path and
# link their appropriate functions

from django.urls import path
from . import views

urlpatterns = [
    path('', views.create_report),
    path('', views.delete_report),
    path('', views.get_report),
    path('', views.list_report),
    path('', views.update_report),
    path('', views.submit_report),
    path('', views.update_section),
    path('', views.create_account),
    path('', views.login),
    path('', views.logout),
]
