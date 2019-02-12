# Link report and account functionality to views

from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from . import views

urlpatterns = [
    path('report', views.report),
    path('reports', views.reports),
    path('report/<int:report_pk>', views.report_detail),
    path('report/<int:report_pk>/section/<int:section_pk>', views.section),
    path('submit_report/<int:report_pk>', views.submit_report),
]

urlpatterns = format_suffix_patterns(urlpatterns)
