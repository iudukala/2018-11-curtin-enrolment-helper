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
            all_plan = StudentUnit.objects.all().filter(StudentID=student).order_by('Year', 'Semester')
            plans = form_plans(all_plan)
            resp = return_resp(courses, templates, plans)
        except (Student.DoesNotExist, CourseTemplate.DoesNotExist, StudentUnit.DoesNotExist) as e:
            error_msg = 'Invalid data input'
            return HttpResponse(error_msg)
    else:
        raise Http500()

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
    year = []
    semester_1 = []
    semester_2 = []
    this_semester = -1
    this_year = -1

    for temp in all_course_temp:
        course_options = CourseTemplateOptions.objects.all().filter(Option=temp.Option).order_by('Year', 'Semester')
        for opt in course_options:
            single_unit = Unit.objects.get(UnitID=opt.UnitID.UnitID)
            student = Student.objects.get(pk=student_id)
            try:
                student_unit = StudentUnit.objects.get(StudentID=student, UnitID=opt.UnitID)
                unit = {'id' : single_unit.UnitID, 'name' : single_unit.Name, 'credits' : single_unit.Credits, 'status' : student_unit.Status, 'attempts' : student_unit.Attempts}
            except StudentUnit.DoesNotExist:
                unit = {'id' : single_unit.UnitID, 'name' : single_unit.Name, 'credits' : single_unit.Credits, 'status' : 1, 'attempts' : 0}

            if this_year is -1 and this_semester is -1:
                this_year = opt.Year
                this_semester = opt.Semester
            if opt.Year is this_year and opt is not course_options[len(course_options)-1]:
                if opt.Semester is 1:
                    semester_1.append(unit)
                elif opt.Semester is 2:
                    semester_2.append(unit)
            elif (opt.Year - this_year) is 1:
                if not semester_1:
                    year.append(semester_2)
                elif not semester_2:
                    year.append(semester_1)
                else:
                    year.append(semester_1)
                    year.append(semester_2)
                semester_1 = []
                semester_2 = []
                templates.append(year)
                year = []
                this_year = opt.Year
                this_semester = opt.Semester
                if opt.Semester is 1:
                    semester_1.append(unit)
                elif opt.Semester is 2:
                    semester_2.append(unit)
            elif opt is course_options[len(course_options)-1] and opt.Year is this_year:
                if opt.Semester is 1:
                    semester_1.append(unit)
                elif opt.Semester is 2:
                    semester_2.append(unit)

                if not semester_1:
                    year.append(semester_2)
                elif not semester_2:
                    year.append(semester_1)
                else:
                    year.append(semester_1)
                    year.append(semester_2)

                templates.append(year)

    return templates


def form_plans(all_plans):
	plan = []
	year = []
	semester_1 = []
	semester_2 = []
	this_semester = -1
	this_year = -1
	for pl in all_plans:
		single_unit = Unit.objects.get(UnitID=pl.UnitID.UnitID)
		unit = {'id':single_unit.UnitID, 'credits':single_unit.Credits}
		if this_year is -1 and this_semester is -1:
			this_year = pl.Year
			this_semester = pl.Semester
		if pl.Year is this_year and pl is not all_plans[len(all_plans)-1]:
			if pl.Semester is 1:
				semester_1.append(unit)
			elif pl.Semester is 2:
				semester_2.append(unit)
		elif (pl.Year - this_year) is 1:
			if not semester_1:
				year.append(semester_2)
			elif not semester_2:
				year.append(semester_1)
			else:
				year.append(semester_1)
				year.append(semester_2)
				semester_1 = []
				semester_2 = []
				plan.append(year)
				year = []
				this_year = pl.Year
				this_semester = pl.Semester
				if pl.Semester is 1:
					semester_1.append(unit)
				elif pl.Semester is 2:
					semester_2.append(unit)
		elif pl is all_plans[len(all_plans) - 1] and pl.Year is this_year:
			if pl.Semester is 1:
				semester_1.append(unit)
			elif pl.Semester is 2:
				semester_2.append(unit)
			if not semester_1:
				year.append(semester_2)
			elif not semester_2:
				year.append(semester_1)
			else:
				year.append(semester_1)
				year.append(semester_2)
				plan.append(year)

	return plan
######################################################################################################






from django.shortcuts import render
from django.shortcuts import redirect
from django.contrib.auth import authenticate
from django.contrib.auth import login
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.core import serializers
from django.shortcuts import render
from django.core.files import File
from .models import Student
# from django.utils import simple

import json
from .pdf_validator import PdfValidator
from .student_information_saver import StudentInformationSaver
from core_app.temp_populating_database import populate, delete_database


def index(request):
    """
    Default Index page
    """
    return HttpResponse("At the core_app page")


# TODO: Return 'success' (parsedInfo is Valid)
# TODO: Return 'failed' (What is required to be returned?)
@login_required
def upload_file(request):
    """
    Handles pdf files being uploaded.
    https://docs.djangoproject.com/en/1.10/topics/http/file-uploads/
    """
    print(request)

    if request.method == 'POST':
        if request.FILES.get('file[]'):

            myfile = request.FILES.get('file[]')
            file = File(myfile)
            validator = PdfValidator(file)
            valid, output_message = validator.pdf_is_valid()
            if valid:
                information_saver = StudentInformationSaver(validator.get_validated_information())
                information_saver.set_student_units()
                print(information_saver.output_message)
                return HttpResponse(status=200)
            else:
                print(validator.output_message)
                return HttpResponse("Validation or saving student error.", status=500)

        else:
            return HttpResponse("Request is not correct.", status=403)

    else:
        return HttpResponse("Validation or saving student error.", status=403)


@login_required
def get_student_list(request):
    """
    :param request:
    :return: A JSON dict object of StudentID and name
    """
    if request.method == 'GET':

        return_list = list(Student.objects.all().values('StudentID', 'Name'))
        return HttpResponse(json.dumps(return_list), content_type='application/list')

    else:
        return HttpResponse("Request Error", status=400)


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

@login_required
def report_upload(request):
    return render(request, 'core_app/report_upload.html')

@login_required
def home(request):
    return render(request, 'core_app/home.html')


@login_required
def planner(request):
    return render(request, 'core_app/planner.html')
