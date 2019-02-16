from rest_framework.decorators import api_view, parser_classes
from django.http import JsonResponse
from .models import *
from .policy import pol
import os
from rest_framework.exceptions import ParseError
from rest_framework.parsers import FileUploadParser, MultiPartParser

def get_report(report_pk):
    """
    Returns a python object representation of the specified section.
    
    report_pk -- ID of the report to compile.
    """
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

def get_sections(r_id):
    """
    Returns a python object array of sections for the specified report.

    r_id -- ID of the report to compile sections for.
    """
    # create a dict of arrays for section
    section_set = {"sections": []}
    queryset = Section.objects.filter(report_id=r_id)
    for index in range(len(queryset)):
        i = queryset[index]
        data = {
            "id": i.id,
            "completed": i.completed,
            "title": i.title,
            "html_description": i.html_description,
            "rule_violations": [],
        }
        # append the fields for corresponding section
        data.update(get_fields(i.id))
        # process rules from the policy file if the section is completed
        if i.completed:
            rules = pol.sections[index].rules
            for rule in rules:
                try:
                    named_fields = generate_named_fields_for_section(data['fields'])
                    if not rule['rule'](data, named_fields):
                        info = {
                            "label": rule['title'],
                            "rule_break_text": rule['rule_break_text'],
                        }
                        data['rule_violations'].append(info)
                except Exception as e:
                    print('Rule "{}" encountered an error. {}'.format(rule['title'], e))
        # append section to the array
        section_set["sections"].append(data.copy())

    return section_set

def get_fields(s_id):
    """
    Returns a python object array of fields for the specified section.

    s_id -- ID of the section to compile fields for.
    """
    # create dict of arrays for fields
    field_set = {"fields": []}
    queryset = Field.objects.filter(section_id=s_id).order_by('number')

    for i in queryset:
        # function that gets the corresponding datatype
        value = Field.get_datatype(i)
        data = {
            "completed": i.completed,
            "field_name": i.field_name,
            "label": i.label,
            "field_type": i.field_type,
            "number": i.number,
            "value": value,
            "id": i.id,
        }
        # append the fields to array
        # use copy() to avoid overwriting
        field_set["fields"].append(data.copy())

    return field_set


def generate_named_fields_for_section(fields):
    """
    Prepares a dictionary of key-value pairs based on the raw fields
    passed in. Used to pass into the rule lambda functions.

    fields -- Python object prepared by get_fields
    """
    result = {}
    for field in fields:
        key = field['field_name']
        value = field['value']
        result[key] = value
    return result

@api_view(['POST'])
def report(request):
    """
    Generates a new empty report for the current user and returns it
    in json format. The title of the report should be provided as
    follows:
    {
        "title": "Report Title Here"
    }
    """
    # Create the report
    report = Report.objects.create(user_id=request.user, title=request.data['title'],
                                   date_created=datetime.date.today())
    report.save()

    # Create the sections
    for i in range(len(pol.sections)):
        section = pol.sections[i]
        s = Section.objects.create(report_id=report, auto_submit=section.auto_submit,
                                   required=section.required, completed=False,
                                   title=section.title, html_description=section.html_description,
                                   number=i)
        s.save()

        # Create the fields
        for key in section.fields:
            field = section.fields[key]
            f = Field.objects.create(section_id=s, field_name=key, label=field['label'],
                                     number=field['number'], field_type=field['field_type'], completed=False)
            f.save()
    
    # Return the newly created report
    data = get_report(report.id)
    return JsonResponse(data)

@api_view(['GET'])
def reports(request):
    """
    Returns a condensed version of the current user's reports in json
    format.
    """
    report_set = {"reports": []}
    queryset = Report.objects.all().filter(user_id=request.user.id).order_by('date_created')
    for i in queryset:
        data = {
            "user_id": request.user.id,
            "report_pk": i.id,
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
    """
    Handler for individual report actions. Actions are divided into
    GET, PUT, and DELETE requests.

    report_pk -- ID of the report to carry out the action on.
    """
    # GET: Retrieves a json representation of the specified report
    if request.method == 'GET':
        data = get_report(report_pk)
        return JsonResponse(data)

    # PUT: Submits a report to the administrator for review,
    # and marks it as "submitted", after which changes may
    # not be made.
    elif request.method == 'PUT':
        return JsonResponse({"message": "Report submitted."})

    # DELETE: Deletes a report from the user's account.
    elif request.method == 'DELETE':
        # get corresponding sections
        section_set = Section.objects.filter(report_id=report_pk)
        for i in section_set:
            # gets the fields that only have a data file in them
            field_set = Field.objects.filter(section_id=i.id).exclude(data_file__exact='')
            if field_set.exists():
                for j in field_set:
                    # delete the file if exists
                    path_name = str(j.data_file)
                    os.remove(path_name)
        # delete the full report and catch the title
        r = Report.objects.get(id=report_pk)
        title = r.title
        r.delete()
        return JsonResponse({"message": "Deleted report: {0}.".format(title)})

@api_view(['PUT'])
def section(request, report_pk, section_pk):
    """
    Updates the specified section with new data.

    section_pk -- Section for which the data should be updated.
    """
    for key in request.data:
        # get the matching field object
        update = Field.objects.get(section_id=section_pk, field_name=key)

        if update.field_type == "boolean":
            # flight check
            if request.data[key] == "true":
                update.data_bool = True
            elif request.data[key] == "false":
                update.data_bool = False
            update.completed = True

        if update.field_type == "decimal":
            # initialize to 0
            if (
                    request.data[key] == "" or
                    request.data[key] is None
            ):
                update.data_decimal = 0.0
            else:
                update.completed = True
                update.data_decimal = request.data[key]

        if update.field_type == "date":
            # initialize to today's date
            if (
                    request.data[key] == "" or
                    request.data[key] is None
            ):
                update.data_date = None
            else:
                update.completed = True
                update.data_date = request.data[key]

        if update.field_type == "file":
            if not(
                    request.data[key] == "" or
                    request.data[key] is None
            ):
                update.completed = True
                update.data_file = request.data[key]

        if update.field_type == "string":
            if not(
                    request.data[key] == "" or
                    request.data[key] is None
            ):
                update.completed = True
                update.data_string = request.data[key]


        if update.field_type == "integer":
            # initialize to 0
            if (
                    request.data[key] == "" or
                    request.data[key] is None
            ):
                update.data_integer = 0
            else:
                update.completed = True
                update.data_integer = request.data[key]

        update.save()

    # update section boolean to complete
    complete = section_complete(section_pk)
    s = Section.objects.get(id=section_pk)
    if complete:
        s.completed = True
    else:
        s.completed = False
    s.save()

    # get section and field details
    data = {
        "id": s.id,
        "completed": s.completed,
        "title": s.title,
        "html_description": s.html_description,
        "rule_violations": [],
    }
    data.update(get_fields(s.id))
    # process rules from the policy file if the section is completed
    if s.completed:
        rules = pol.sections[s.number].rules
        for rule in rules:
            try:
                named_fields = generate_named_fields_for_section(data['fields'])
                if not rule['rule'](data, named_fields):
                    info = {
                        "label": rule['title'],
                        "rule_break_text": rule['rule_break_text'],
                    }
                    data['rule_violations'].append(info)
            except Exception as e:
                print('Rule "{}" encountered an error. {}'.format(rule['title'], e))
    return JsonResponse(data)

def section_complete(section_pk):
    """
    Returns True if any fields of the specified section have been
    entered by the user. This means that entering even one field
    will count the entire section as "complete".

    section_pk -- ID of the section whose fields you wish to check.
    """
    # grab field set
    check_fields = Field.objects.filter(section_id=section_pk)

    # return true if any field is complete
    for i in check_fields:
        if i.completed:
            return True
    return False
