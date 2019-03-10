# Link report and account functionality to views

from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from . import views

urlpatterns = [
    path('report', views.create_report),
    path('reports', views.reports),
    path('report/<int:report_pk>', views.report_detail),
    path('report/<int:report_pk>/final', views.finalize_report),
    path('section/<int:section_pk>', views.section),
]

urlpatterns = format_suffix_patterns(urlpatterns)
