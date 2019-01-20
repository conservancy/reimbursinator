# Rupika Dikkala
# January 19, 2019
# Add urls and link to the
# views

from django.urls import path
from . import views

urlpatterns = [
    path('create_report/', views.create_report),
    path('delete_report/', views.delete_report),
    path('get_report/', views.get_report),
    path('list_report/', views.list_report),
    path('update_report/', views.update_report),
    path('submit_report/', views.submit_report),
    path('update_section/', views.update_section),
    path('create_account/', views.create_account),
    path('login/', views.login),
    path('logout/', views.logout),
]
