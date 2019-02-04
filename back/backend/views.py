from rest_framework import generics
from rest_framework import status
from rest_framework.decorators import api_view
from django.shortcuts import render
from django.http import JsonResponse
from .models import *
from .serializers import *

# Sample view using generics

class List(generics.ListCreateAPIView):
    queryset = Report.objects.all()
    serializer_class = ReportSerializer

class Detail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Report.objects.all()
    serializer_class = ReportSerializer

# API Endpoints

@api_view(['POST'])
def report(request):
    '''
    Generate a new empty report and return it
    '''
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

@api_view(['GET'])
def reports(request):
    print("User: ", request.user)
    print("User id: ", request.user.id)
    data = {
        "reports": [
            {
                "report_pk": 1,
                "title": "2018 Portland trip",
                "date_created": "2018-05-22T14:56:28.000Z",
                "state": "created",
                "date_submitted": "0000-00-00T00:00:00.000Z"
            },
            {
                "report_pk": 2,
                "title": "2017 Los Angeles trip",
                "date_created": "2017-05-22T14:56:28.000Z",
                "state": "submitted",
                "date_submitted": "2017-07-22T14:56:28.000Z"
            },
            {
                "report_pk": 3,
                "title": "2017 Denver trip",
                "date_created": "2015-04-22T14:56:28.000Z",
                "state": "accepted",
                "date_submitted": "2015-06-22T14:56:28.000Z"
            }
        ]
    }
    return JsonResponse(data)

@api_view(['GET', 'PUT', 'DELETE'])
def report_detail(request, report_pk):
    if request.method == 'GET':
        data = {
            "report_pk": report_pk,
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
    elif request.method == 'PUT':
        return JsonResponse({"message": "Report submitted."})
    elif request.method == 'DELETE':
        return JsonResponse({"message": "Deleted report {0}.".format(report_pk)})

@api_view(['PUT'])
def section(request, report_pk, section_pk):
    '''
    Update a section with new data.
    '''
    data = {
        "message": "Updated report {0}, section {1}.".format(report_pk, section_pk),
        "fields": {
            "international": True,
            "travel_date": "2012-04-23T18:25:43.511Z",
            "fare": "1024.99",
            "lowest_fare_screenshot": "image",
        }
    }
    return JsonResponse(data)
