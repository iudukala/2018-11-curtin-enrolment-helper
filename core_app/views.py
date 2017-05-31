from .models import Student, StudentUnit, CourseTemplate, CourseTemplateOptions, Unit, Equivalence, Prerequisite, Options
import json


###############################################################################
#
#
###############################################################################
def enrol_plan_validity(request):
    # If all good then add units to completedUnits array waiting to save
    valid_enrol_units = []

    if student_id is not -1 and request.is_ajax():
        try:
            received_plan_json = json.loads(request.body.decode('utf-8'))
        except Student.DoesNotExist:
            raise RuntimeError('errors: can not parse json object') from error
        try:
            boolean_respond = validity_query(received_plan_json, valid_enrol_units, student_id)
        except Student.DoesNotExist:
            raise RuntimeError('') from error
    else:
        raise Http500()

    return boolean_respond

###############################################################################
#
#
###############################################################################
def validity_query(received_plan_json, valid_enrol_units, student_id):
    for year in received_plan_json:
        this_year = received_plan_json.index(year)
        for semester in year:
            this_semester = year.index(semester)
            credits_this_semester = 0
            for unit in semester:
                unit_id = unit['id']
                credit = unit['credits']
                if unit_id is not 'ELECTIVE':
                    this_student = Student.objects.get(StudentID=student_id)
                    this_student_course = Course.objects.get(CourseID=this_student.CourseID.CourseID)

                    single_unit = Unit.objects.get(UnitID=unit_id)
                    course_temps = CourseTemplate.objects.get(CourseID=this_student_course)
                    equiv_units = Equivalence.objects.get(UnitID=single_unit)
                    course_temp_option = None
                    for temp in course_temps:
                        try:
                            course_temp_option = CourseTemplateOptions.objects.get(UnitID=single_unit, Option=temp)
                            break
                        except CourseTemplateOptions.DoesNotExist:
                            continue

                    if course_temp_option is None:
                        return False

                    # the units in enrolplan could be either temp units or plan units
                    try:
                        # this is previous plan unit
                        completed_unit = StudentUnit.objects.get(StudentID=this_student, UnitID=single_unit)
                        # here will need to generate an error message to denote what problems are with enrollment (elif)
                        if completed_unit.Status is 2 or course_temp_option.Year is not this_year or course_temp_option.Semester is not this_semester:
                            valid_enrol_units = []
                            return False
                        else:
                            credits_this_semester += credit
                            valid_enrol_units.append(unit_id)
                    # this is course temp unit
                    except StudentUnit.DoesNotExist:
                        if course_temp_option.Year is not this_year or course_temp_option.Semester is not this_semester:
                            valid_enrol_units = []
                            return False

                        # check if the equivalence already existed in the previous student plan and passed it
                        try:
                            unit_status = StudentUnit.objects.get(StudentID=this_student, UnitID=equiv_units).Status
                            if unit_status is 2:
                                valid_enrol_units = []
                                return False
                        # no equivalence units in previous enrolment plan
                        except StudentUnit.DoesNotExist:
                            # checking prerequisite if it has been achieved
                            prerequisites = Prerequisite.objects.get(UnitID=single_unit)

                            for pre in prerequisites:
                                opts = Options.objects.get(Option=prerequisites)


                            for opt in opts:
                                # if can not find the prerequisite unit in student plan that means does not enrol prerequisite before
                                if not StudentUnit.objects.get(UnitID=opt.UnitID.UnitID):
                                    valid_enrol_units = []
                                    return False
                                # check the prerequisite if passed or failed in previous student plan
                                a_unit = StudentUnit.objects.get(UnitID=opt.UnitID.UnitID)
                                if a_unit.Status is not 2:
                                    valid_enrol_units = []
                                    return False
                                # if all good add this temp unit and add up credits
                                credits_this_semester += credit
                                valid_enrol_units.append(unit_id)

            # Credit amount per semester musn't exceed 100
            if credits_this_semester > 100:
                valid_enrol_units = []
                return False

    return True
###############################################################################





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

def planner(request):
    return render(request, 'core_app/planner.html');
