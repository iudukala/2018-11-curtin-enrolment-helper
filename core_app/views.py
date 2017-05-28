from core_app.models import Student, StudentUnit, Course, CourseTemplate, CourseTemplateOptions, Unit
from django.http import HttpResponse
from django.http import JsonResponse
import json

######################################################################################################
# For retrieving the student course progress information, 1st get the student id
# from request with json object, and retrieving the data from data model and forming
# the new json object return back to the Front-end
######################################################################################################
def course_progress(request):
    resp = {}
    if request.is_ajax():
        try:
            received_data = json.loads(request.body.decode('utf-8'))
        except ValueError:
            error_msg = 'can not parse json object'
            return HttpResponse(error_msg)
        try:
            student_id = received_data.get['id']
            student = Student.objects.get(pk=student_id)
            courses = form_course(student)
            all_course_temp = CourseTemplate.objects.all().filter(CourseID=student.CourseID)
            templates= form_templates(all_course_temp, student_id)
            # need student instance
            all_plan = StudentUnit.objects.all().filter(StudentID=student).order_by('Year', 'Semester')

            plans = form_plans(all_plan)
            resp = return_resp(courses, templates, plans)
        except Student.DoesNotExist:
            error_msg = 'wrong student ID input'
            return HttpResponse(error_msg)
    else:
        raise Http404()

    return JsonResponse(resp)

######################################################################################################
# Form the json object
# the final output should be like {course:<courses>, template:<templates>, plan:<plans>}
######################################################################################################
def return_resp(courses, templates, plans):
    resp = {
        'course' : courses,
        'template' : templates,
        'plan' : plans
    }

    return resp

######################################################################################################
# Finding each data as required and save and construct with the pre-defined
# json data, for both template_option and plans, i.e. courses :{name:<>, id:<>}
# templates = [[[{id:<>, name:<>, credits:<>,status:<>, attempts:<>}]]] and plans same as templates
######################################################################################################
def form_course(student):
    course_id = student.CourseID.CourseID
    student_course = Course.objects.get(CourseID=course_id)
    courses = {'name' : student_course.Name, 'id' : course_id}

    return courses

def form_templates(all_course_temp, student_id):
    templates = []

    for temp in all_course_temp:
        course_options = CourseTemplateOptions.objects.all().filter(Option=temp.Option).order_by('Year', 'Semester')
        for opt in course_options:
            semester = []
            year = []
            #if 'ELECTIVE' in opt.UnitID.unitCode
                # Search for a unit in StudentUnits which has;
                #   - The elective flag set to True
                #   - The same amount of credits as opt.UnitID.Credits
                #   - Isnt in the 'excluded array'
                # Add that unit object to 'excluded'
            single_unit = Unit.objects.get(UnitID=opt.UnitID.UnitID)    #  !!!!!!!!!! unit id changed , actually this is passed an object rathera than ID
            student = Student.objects.get(pk=student_id)
            try:
                student_unit = StudentUnit.objects.get(StudentID=student, UnitID=opt.UnitID)
                unit = {'id' : single_unit.UnitID, 'name' : single_unit.Name, 'credits' : single_unit.Credits, 'status' : student_unit.Status, 'attempts' : student_unit.Attempts}
            except StudentUnit.DoesNotExist:
                unit = {'id' : single_unit.UnitID, 'name' : single_unit.Name, 'credits' : single_unit.Credits, 'status' : 1, 'attempts' : 0}
            semester.append(unit)
            year.append(semester)
            templates.append(year)

    return templates

def form_plans(all_plans):
    plans = []

    for pl in all_plans:
        semester = []
        year = []
        # credit version unit id
        single_unit = Unit.objects.get(UnitID=pl.UnitID.UnitID) # !!!!!! issue
        unit = {'id':single_unit.UnitID, 'credits':single_unit.Credits}

        # make sure would not get wrong index
        # last_item_index = len(semseter) - 1
        # if

        semester.append(unit)
        year.append(semester)
        plans.append(year)

    return plans
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
