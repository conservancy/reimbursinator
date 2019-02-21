from rest_framework.decorators import api_view
from django.http import JsonResponse, HttpResponse
from .models import *
from .policy import pol
from django.core.mail import send_mail
from django.template.loader import render_to_string
import html2text
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
    queryset = Field.objects.filter(section_id=s_id).order_by('number')

    for i in queryset:
        # function that gets the corresponding datatype
        value = Field.get_datatype(i)
        data = {
            "field_name": i.field_name,
            "label": i.label,
            "type": i.type,
            "number": i.number,
            "value": value
        }
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
        j = 0
        for key in section.fields:
            field = section.fields[key]
            f = Field.objects.create(section_id=s, field_name=key, label=field['label'],
                                     number=j, type=field['type'], completed=False)
            f.save()
            j = j+1
    
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


#TODO:
# Show broken rules
# Attach image files
# Also send email to user
def submit_report(request, report_pk):
    ''' Send a formatted email of the report given by 'report_pk' to the
        reimbursinator email address.
    '''
    params = get_reports(report_pk)
    msg_html = render_to_string('backend/email.html', params)
    msg_plain = render_to_string('backend/email.txt', params)
    #msg_plain = html2text.html2text(msg_html)

    send_mail('Report #'+str(report_pk), #subject
              msg_plain, #body
              'no_effect', #from:
              ['reimbursinator@gmail.com',], #to:
              html_message=msg_html)

    return HttpResponse(status=200, content="Thanks for submitting your report.")

submit_report('GET',21)
