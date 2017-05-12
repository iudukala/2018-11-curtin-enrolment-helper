from .models import Student, StudentUnit, CourseTemplate
from django.http import JsonResponse
import json


######################################################################################################
# For retrieving the student course progress information, 1st get the student id
# from request with json object, and retrieving the data from data model and forming
# the new json object return back to the Front-end
######################################################################################################
def course_progress(request):
    if request.is_ajax():
        try:
            received_data = json.loads(request.body.decode('utf-8'))
        except Student.DoesNotExist:
            raise error_message = 'errors json object'
        try:
            student_id = received_data.get['id']
            student = Student.objects.get(pk=student_id)
            all_template = CourseTemplate.objects.all().filter(CourseID=student.CourseID).values()
            all_plan = StudentUnit.objects.all().filter(StudentID=student.StudentID).values()
        except Student.DoesNotExist:
            raise error_message = 'wrong student ID'
    else:
        raise Http404()

    templates = form_templates(all_template)
    plans = form_plans(all_plan)
    resp = return_couseTemp(templates, plans)

    return JsonResponse(resp)

######################################################################################################
# Form the json object
######################################################################################################
def return_resp(templates, plans):
    resp = {
        'template': templates
        'plan': plans
    }

    return resp

######################################################################################################
# Finding each data as required and save and construct with the pre-defined
# json data, for both templates and plans
######################################################################################################
def form_templates(all_template):
    templates = {}
    years = {}
    semesters = {}
    for temp in all_template:
        templates[temp.Year] = temp.Semester
        years[temp.Semester] = temp.UnitID
        single_unit = Unit.object.get(pk=temp.UnitID)
        semesters[temp.UnitID] = {'name':single_unit.Name, 'credits':single_unit.Credits}

    return templates

def form_plans(all_plans):
    plans = {}
    years = {}
    semesters = {}
    for plan in all_plans:
        templates[plan.Year] = plan.Semester
        years[plan.Semester] = plan.UnitID
        single_unit = Unit.object.get(pk=plan.UnitID)
        semesters[plan.UnitID] = {'name':single_unit.Name, 'credits':single_unit.Credits, 'attempts':plan.Attempts}

    return plans
######################################################################################################
