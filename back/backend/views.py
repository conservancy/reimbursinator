from rest_framework.decorators import api_view
from django.http import JsonResponse
from .models import *
from .policy import pol
import os


# function that prints all the reports
def get_reports(report_pk):
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

# function that gets all the fields
# takes section_id param
def get_fields(s_id):
    # create dict of arrays for fields
    field_set = {"fields": []}
    queryset = Field.objects.filter(section_id=s_id).order_by('number')

    for i in queryset:
        # function that gets the corresponding datatype
        value = Field.get_datatype(i)
        data = {
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
    result = {}
    for field in fields:
        key = field['field_name']
        value = field['value']
        result[key] = value
    return result

# API Endpoints
@api_view(['POST'])
def report(request):
    '''
    Generate a new empty report and return it
    '''
    
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
    data = get_reports(report.id)
    return JsonResponse(data)

# View the list of reports
@api_view(['GET'])
def reports(request):
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


# actions for an individual report
@api_view(['GET', 'PUT', 'DELETE'])
def report_detail(request, report_pk):
    # view the report
    if request.method == 'GET':
        data = get_reports(report_pk)
        return JsonResponse(data)

    # submit the report
    elif request.method == 'PUT':
        return JsonResponse({"message": "Report submitted."})

    # Delete the report
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


# update a section with new data
@api_view(['PUT'])
def section(request, report_pk, section_pk):

    for key in request.data:
        # get the matching field object
        update = Field.objects.get(section_id=section_pk, field_name=key)

        if update.field_type == "boolean":
            # flight check
            if request.data[key] == "true":
                update.data_bool = True
            elif request.data[key] == "false":
                update.data_bool = False

        if update.field_type == "decimal":
            # initialize to 0
            if (
                    request.data[key] == "" or
                    request.data[key] is None
            ):
                update.data_decimal = 0.0
            else:
                update.data_decimal = request.data[key]

        if update.field_type == "date":
            # initialize to today's date
            if (
                    request.data[key] == "" or
                    request.data[key] is None
            ):
                update.data_date = None
            else:
                update.data_date = request.data[key]

        if update.field_type == "file":
            update.data_file = request.data[key]

        if update.field_type == "string":
            update.data_string = request.data[key]

        if update.field_type == "integer":
            # initialize to 0
            if (
                    request.data[key] == "" or
                    request.data[key] is None
            ):
                update.data_integer = 0
            else:
                update.data_integer = request.data[key]

        update.save()

    # update section boolean to complete
    complete = section_complete(section_pk)
    s = Section.objects.get(id=section_pk)
    if complete:
        # s = Section.objects.get(id=section_pk)
        s.completed = True
        s.save()

    data = {
        "message": "Updated report {0}, section {1}.".format(report_pk, section_pk),
        "section completion": s.completed,
        "request_data": request.data
    }
    return JsonResponse(data)

# function checks if a field is filled and
# returns boolean accordingly
def section_complete(section_pk):
    # grab field set
    check_fields = Field.objects.filter(section_id=section_pk)

    # return true if any field is filled
    for i in check_fields:
        if i.field_type == "boolean":
            if not(
                    i.data_bool == "" or
                    i.data_bool is None
            ):
                return True
        elif i.field_type == "decimal":
            if not(
                    i.data_decimal == 0.0 or
                    i.data_decimal == "" or
                    i.data_decimal is None
            ):
                return True
        elif i.field_type == "date":
            if not(
                    i.data_date == "" or
                    i.data_date is None
            ):
                return True
        elif i.field_type == "file":
            if not(
                    i.data_file == "" or
                    i.data_file is None
            ):
                return True
        elif i.field_type == "string":
            if not(
                    i.data_string == "" or
                    i.data_string is None
            ):
                return True
        elif i.field_type == "integer":
            if not(
                    i.data_integer == 0 or
                    i.data_integer == "" or
                    i.data_integer is None
            ):
                return True

    # return false if no field is filled
    return False
