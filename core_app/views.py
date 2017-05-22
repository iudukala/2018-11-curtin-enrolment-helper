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
            course_temp = CourseTemplate.objects.get(CourseID=student.CourseID)
            all_template_option = CourseTemplateOptions.objects.all().filter(Option=course_temp.Option)
            all_plan = StudentUnit.objects.all().filter(StudentID=student.StudentID)
        except Student.DoesNotExist:
            raise RuntimeError('errors: wrong student ID input') from error
    else:
        raise Http404()

    template_options = form_templates(all_template_option)
    plans = form_plans(all_plan)
    resp = return_couseTemp(template_options, plans)

    return JsonResponse(resp)

######################################################################################################
# Form the json object
######################################################################################################
def return_resp(template_options, plans):
    resp = {
        'template_option': template_options
        'plan': plans
    }

    return resp

######################################################################################################
# Finding each data as required and save and construct with the pre-defined
# json data, for both template_option and plans, i.e.# template = {'1':{'2':{'16102183':'SE200', 'credits',:'25'}}}
######################################################################################################
def form_templates(all_template_option):
    template_option = {}
    for temp in all_template_option:
        single_unit = Unit.object.get(pk=temp.UnitID)
        unit = {'name':single_unit.Name, 'credits':single_unit.Credits}
        semester[unit.UnitID] = unit
        semester_info = temp.Semester
        year_info = temp.Year
        template_option.update({year_info:{semester_info:semester}})

    return template_option

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




from django.shortcuts import render
from django.shortcuts import redirect
from django.contrib.auth import authenticate
from django.contrib.auth import login
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required


# Create your views here.
def login_user(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                return render(request, 'core_app/home.html', context=None)
            else:
                return render(request, 'core_app/login.html', {'error_message': 'Your account has been disabled'})
        else:
            return render(request, 'core_app/login.html', {'error_message': 'Invalid login'})
    return render(request, 'core_app/login.html')


@login_required
def logout_user(request):
    logout(request)
    return render(request, 'core_app/login.html')


def report_upload(request):
    return render(request, 'core_app/report_upload.html')


def home(request):
    return render(request, 'core_app/home.html')
