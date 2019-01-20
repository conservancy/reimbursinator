# Rupika Dikkala
# January 19, 2019
# Creating views for URL that
# returns JSON data

from django.shortcuts import render
from django.http import JsonResponse


# Create Report
def create_report(request):
    data = {
        'name': 'create report',
    }
    return JsonResponse(data)

# Delete report
def delete_report(request):
    data = {
        'name': 'Delete report',
    }
    return JsonResponse(data)

# Get report
def get_report(request):
    data = {
        'name': 'get report',
    }
    return JsonResponse(data)

# List Reports
def list_report(request):
    data = {
        'name': 'list report',
    }
    return JsonResponse(data)

# Update Reports
def update_report(request):
    data = {
        'name': 'update report',
    }
    return JsonResponse(data)

# Submit Reports
def submit_report(request):
    data = {
        'name': 'submit report',
    }
    return JsonResponse(data)

# Update section
def update_section(request):
    data = {
        'name': 'update section',
    }
    return JsonResponse(data)


# Create account
def create_account(request):
    data = {
        'name': 'create account',
    }
    return JsonResponse(data)

# Login
def login(request):
    data = {
        'name': 'login',
    }
    return JsonResponse(data)

# Logout
def logout(request):
    data = {
        'name': 'logout',
    }
    return JsonResponse(data)

