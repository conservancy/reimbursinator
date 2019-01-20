# Rupika Dikkala
# January 19, 2019
# Creating views for URL that
# returns JSON data

from django.shortcuts import render
from django.http import JsonResponse


# Create Report
def create_report(request):
    data = {
        "title": "2018 Portland trip",
        "date_created": "2018-05-22T14:56:28.000Z",
        "submitted": False,
        "date_submitted": "0000-00-00T00:00:00.000Z",
        "sections": [
            {
                "id": 1,
                "completed": True,
                "title": "Flight Info",
                "html_description": "<p>Enter flight details here.</p>",
                "fields": {
                    "international": {
                        "label": "International flight",
                        "type": "boolean",
                        "value": True
                    },
                    "travel_date": {
                        "label": "Travel start date",
                        "type": "date",
                        "value": "2016-05-22T14:56:28.000Z"
                    },
                    "fare": {
                        "label": "Fare",
                        "type": "decimal",
                        "value": "1024.99"
                    },
                    "lowest_fare_screenshot": {
                        "label": "Lowest fare screenshot",
                        "type": "file",
                        "value": "e92h842jiu49f8..."
                    },
                    "plane_ticket_invoice": {
                        "label": "Plane ticket invoice PDF",
                        "type": "file",
                        "value": ""
                    }
                },
                "rule_violations": [
                    {
                        "error_text": "Plane ticket invoice must be submitted."
                    }
                ]
            },
            {
                "id": 2,
                "completed": False,
                "title": "Hotel info",
                "html_description": "<p>If you used a hotel, please enter the details.</p>",
                "fields": {
                    "total": {
                        "label": "Total cost",
                        "type": "decimal"
                    }
                },
                "rule_violations": [
                ]
            }
        ]
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
        "title": "2018 Portland trip",
        "date_created": "2018-05-22T14:56:28.000Z",
        "submitted": False,
        "date_submitted": "0000-00-00T00:00:00.000Z",
        "sections": [
            {
                "id": 1,
                "completed": True,
                "title": "Flight Info",
                "html_description": "<p>Enter flight details here.</p>",
                "fields": {
                    "international": {
                        "label": "International flight",
                        "type": "boolean",
                        "value": True
                    },
                    "travel_date": {
                        "label": "Travel start date",
                        "type": "date",
                        "value": "2016-05-22T14:56:28.000Z"
                    },
                    "fare": {
                        "label": "Fare",
                        "type": "decimal",
                        "value": "1024.99"
                    },
                    "lowest_fare_screenshot": {
                        "label": "Lowest fare screenshot",
                        "type": "file",
                        "value": "e92h842jiu49f8..."
                    },
                    "plane_ticket_invoice": {
                        "label": "Plane ticket invoice PDF",
                        "type": "file",
                        "value": ""
                    }
                },
                "rule_violations": [
                    {
                        "error_text": "Plane ticket invoice must be submitted."
                    }
                ]
            },
            {
                "id": 2,
                "completed": False,
                "title": "Hotel info",
                "html_description": "<p>If you used a hotel, please enter the details.</p>",
                "fields": {
                    "total": {
                        "label": "Total cost",
                        "type": "decimal"
                    }
                },
                "rule_violations": [
                ]
            }
        ]
    }
    return JsonResponse(data)

# List Reports
def list_report(request):
    data = {
        "reports": [
            {
                "title": "2018 Portland trip",
                "date_created": "2018-05-22T14:56:28.000Z",
                "state": "created",
                "date_submitted": "0000-00-00T00:00:00.000Z"
            },
            {
                "title": "2017 Los Angeles trip",
                "date_created": "2017-05-22T14:56:28.000Z",
                "state": "submitted",
                "date_submitted": "2017-07-22T14:56:28.000Z"
            },
            {
                "title": "2017 Denver trip",
                "date_created": "2015-04-22T14:56:28.000Z",
                "state": "accepted",
                "date_submitted": "2015-06-22T14:56:28.000Z"
            }
        ]
    }
    return JsonResponse(data)

# Update Reports
def update_report(request):
    data = {
        'name': 'update report',
        'state': 'SUBMITTED!',
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
        "fields": {
            "international": True,
            "travel_date": "2012-04-23T18:25:43.511Z",
            "fare": "1024.99",
            "lowest_fare_screenshot": "image",
        }
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

