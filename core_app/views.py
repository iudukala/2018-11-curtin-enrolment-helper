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
            raise RuntimeError('errors: can not parse json object') from error
        try:
            student_id = received_data.get['id']
            student = Student.objects.get(pk=student_id)
            all_template = CourseTemplate.objects.all().filter(CourseID=student.CourseID)
            all_plan = StudentUnit.objects.all().filter(StudentID=student.StudentID)
        except Student.DoesNotExist:
            raise RuntimeError('errors: wrong student ID input') from error
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
# json data, for both templates and plans, i.e.# template = {'1':{'2':{'16102183':'SE200', 'credits',:'25'}}}
######################################################################################################
def form_templates(all_template):
    template = {}
    for temp in all_template:
        single_unit = Unit.object.get(pk=temp.UnitID)
        unit = {'name':single_unit.Name, 'credits':single_unit.Credits}
        semester[unit.UnitID] = unit
        semester_info = temp.Semester
        year_info = temp.Year
        template.update({year_info:{semester_info:semester}})

    return template

def form_plans(all_plans):
    plan = {}
    for pl in all_plans:
        single_unit = Unit.object.get(pk=pl.UnitID)
        unit = {'name':single_unit.Name, 'credits':single_unit.Credits, 'attempts':pl.Attemps}
        semester[unit.UnitID] = unit
        semester_info = pl.Semester
        year_info = pl.Year
		plan.update({year_info:{semester_info:semester}})

    return plan
######################################################################################################
