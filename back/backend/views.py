from rest_framework.decorators import api_view
from django.http import JsonResponse
from .models import *


# function that prints all the reports
def get_reports(report_pk):
    # queryset = Report.objects.all()
    queryset = Report.objects.filter(id=report_pk)
    for i in queryset:
        data = {
            "report_pk": report_pk,
            "title": i.title,
            "date_created": i.date_created,
            "submitted": i.submitted,
            "date_submitted": i.date_submitted,
        }
        # append the sections for each report
        data.update(get_sections(i.id))

    # return JsonResponse(data)
    return data

# function that gets all the sections
# takes report_id param
def get_sections(r_id):
    # create a dict of arrays for section
    section_set = {"sections": []}
    queryset = Section.objects.filter(report_id=r_id)
    # queryset = Section.objects.all()
    for i in queryset:
        data = {
            "id": i.id,
            "completed": i.completed,
            "title": i.title,
            "html_description": i.html_description,
        }
        # append the fields for corresponding section
        data.update(get_fields(i.id))
        # append section to the array
        section_set["sections"].append(data.copy())

    return section_set

# function that gets all the fields
# takes section_id param
def get_fields(s_id):
    # create dict of arrays for fields
    field_set = {"fields": []}
    queryset = Field.objects.filter(section_id=s_id)
    # queryset = Field.objects.all()
    for i in queryset:
        data = {i.label: {
            "label": i.label,
            "type": i.type,
            "value": i.number,
        }}
        # append the fields to array
        # use copy() to avoid overwriting
        field_set["fields"].append(data.copy())

    return field_set


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

# List of reports
@api_view(['GET'])
def reports(request):
    report_set = {"reports": []}
    queryset = Report.objects.all()
    for i in queryset:
        data = {
            "title": i.title,
            "date_created": i.date_created,
            "submitted": i.submitted,
            "date_submitted": i.date_submitted,
        }
        # append the sections for each report
        report_set["reports"].append(data.copy())

    return JsonResponse(report_set)


@api_view(['GET', 'PUT', 'DELETE'])
def report_detail(request, report_pk):
    if request.method == 'GET':
        data = get_reports(report_pk)
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

@api_view(['POST'])
def account(request):
    '''
    Create a new user account
    '''
    return JsonResponse({"message": "Account creation successful."})

@api_view(['POST'])
def account_login(request):
    '''
    Log in to a user account
    '''
    return JsonResponse({"message": "Successfully logged in."})

@api_view(['DELETE'])
def account_logout(request):
    '''
    Log out from a user account
    '''
    return JsonResponse({"message": "User logged out."})
