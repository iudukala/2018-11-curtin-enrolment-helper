from .models import Student, StudentUnit, CourseTemplate, CourseTemplateOptions, Unit, Equivalence, Prerequisite, Options, Course
from django.http import HttpResponse
import json


###############################################################################
# For processing the fron-end request checking if the newly created student
# enrollment plan is valid, then will response back the True and generated a
# valid enrolment unit list, otherwise responsing the error message.
#
# Json Structure:
#   {'plan' : [[[{'id' : <UNIT ID>, 'credits' : <UNIT CREDITS>}]]]}
###############################################################################
def enrol_plan_validity(request):
    # If all good then add units to completedUnits array waiting to save
    valid_enrol_units = []
    error_msg = ''
    boolean_respond = False
    # student_id = 16102183, for use as test option
    student_id = -1
    if request.user.is_authenticated():
        student_id = request.user.username
    else:
        error_msg = 'deny invalid user'
        return HttpResponse(error_msg)

    if request.is_ajax() and student_id is not -1:
        try:
            received_plan_json = json.loads(request.body.decode('utf-8'))
            new_plan = received_plan_json['plan']
        except Student.DoesNotExist:
            error_msg = 'can not parse json object'
            return HttpResponse(error_msg)
        boolean_respond = validity_query(new_plan, valid_enrol_units, student_id, error_msg)
    else:
        raise Http500()

    if boolean_respond is False:
        HttpResponse(error_msg)

    return HttpResponse(boolean_respond)

##############################################################################################################################
# Main function for verifying the student plan if valid
# Parameter_1: new student plan passed from fron-end
# Parameter_2: empty list for storing valid unit list
# Parameter_3: student_id for retrieving student object that is for collecting
# course, and then its course templates and course template option based on
# the data model design
#
# Main Algorithm:
#   traversing the new plan list, its structure is like [[[{'id' : <UNIT ID>, 'credits' : <UNIT CREDITS>}]]]
#   1st it isn't Elective unit
#       2nd new enrolled unit is previous enrolled unit
#           - the unit passed or not available current year/semester will return False, otherwise will allow ro add that unit
#       new enrolled unit is never enrolled before
#           3rd check this unit if has equivalence unit and if its equivalence has passed,
#               - if allow to go next then will check if it has prerequisite unit if its prerequisite unit passed
#   it is Elective unit, then add its id and credits
#       - will add this elective unit id and credits
#   4th here will check total credits each semester if exceeded max 100
##############################################################################################################################
def validity_query(new_plan, valid_enrol_units, student_id, error_msg):
    for year in new_plan:
        this_year = new_plan.index(year) + 1

        for semester in year:
            this_semester = year.index(semester) + 1
            credits_this_semester = 0

            for unit in semester:
                unit_id = unit['id']
                credit = unit['credits']
                version = unit['version']
                course_version = unit['its_course_version']
                if unit_id is not 'ELECTIVE':

                    this_student = Student.objects.get(StudentID=student_id)
					# issue 1 also need version
                    this_student_course = Course.objects.get(CourseID=this_student.CourseID.CourseID, Version=course_version)
					# issue 2 may need pass me version
                    single_unit = Unit.objects.get(UnitCode=unit_id, Credits=credit, Version=version)

                    # find this student this course temp and its course temp option so that can retrieve temp unit information
                    course_temps = CourseTemplate.objects.all().filter(CourseID=this_student_course)
                    course_temp_option = None
                    # here will only one course_temp_option be retrieved
                    for temp in course_temps:
                        try:
                            course_temp_option = CourseTemplateOptions.objects.get(UnitID=single_unit, Option=temp)
                        except CourseTemplateOptions.DoesNotExist:
                            continue

                    # return false if no related course option to this enrolled unit (invalid unit in student course temp)
                    if course_temp_option is None:
                        error_msg = 'invalid unit in student course temp'
                        return False


                    # find this student a enrol unit related Equivalence units, otherwise none
                    try:
                        equiv_units = Equivalence.objects.all().filter(UnitID=single_unit)
                    except Equivalence.DoesNotExist:
                        continue

                    # the units in enrolplan could be either temp units or plan units, so will check previous enrolled unit status
                    try:
                        completed_unit = StudentUnit.objects.get(StudentID=this_student, UnitID=single_unit)
                        # here will need to generate an error message to denote what problems are with enrollment (elif)
                        if completed_unit.Status is 2:
                            valid_enrol_units = []
                            error_msg = 'one of unit is passed'
                            return False
                        elif course_temp_option.Year is not this_year:
                            valid_enrol_units = []
                            error_msg = 'one of unit is not available this year'
                            return False
                        elif course_temp_option.Semester is not this_semester:
                            valid_enrol_units = []
                            error_msg = 'one of unit is not available this semester'
                            return False
                        else:
                            credits_this_semester += credit
                            valid_enrol_units.append(unit_id)
                    except StudentUnit.DoesNotExist:
                        if course_temp_option.Year is not this_year or course_temp_option.Semester is not this_semester:
                            valid_enrol_units = []
                            error_msg = 'one of unit is not available this year/semester'
                            return False
                        # here need to check if its equi units have been finished before
                        if equiv_units.exists():
                            # check if the equivalence already existed in the previous student plan and passed it
                            for equiv in equiv_units:
                                try:
                                    unit_status = StudentUnit.objects.get(StudentID=this_student, UnitID=equiv.EquivID).Status
                                    if unit_status is 2:
                                        valid_enrol_units = []
                                        error_msg = 'related equivalence has been finished'
                                        return False
                                # no equivalence units in previous enrolment plan
                                except StudentUnit.DoesNotExist:
                                    prerequisites = Prerequisite.objects.all().filter(UnitID=single_unit)
                                    if prerequisites.exists():
                                        for pre in prerequisites:
                                            opts = Options.objects.get(Option=pre)
                                            for opt in opts:
                                                # if can not find the prerequisite unit in student plan that means does not enrol prerequisite before
                                                try:
                                                    prerequis_unit = StudentUnit.objects.get(StudentID=this_student, UnitID=opt.UnitID.UnitID)
                                                    if prerequis_unit.Status is not 2:
                                                        valid_enrol_units = []
                                                        error_msg = 'did not pass its prerequis unit'
                                                        return False
                                                    elif prerequis_unit.Status is 2:
                                                        credits_this_semester += credit
                                                        valid_enrol_units.append(unit_id)
                                                except StudentUnit.DoesNotExist:
                                                    valid_enrol_units = []
                                                    error_msg = 'has not enrolled its prerequis unit before'
                                                    return False
                                    else:
                                        credits_this_semester += credit
                                        valid_enrol_units.append(unit_id)

                        else:
                            prerequisites = Prerequisite.objects.all().filter(UnitID=single_unit)
                            if prerequisites.exists():
                                for pre in prerequisites:
                                    opts = Options.objects.all().filter(Option=pre)
                                    for opt in opts:
                                        # if can not find the prerequisite unit in student plan that means does not enrol prerequisite before
                                        try:
                                            prerequis_unit = StudentUnit.objects.get(StudentID=this_student, UnitID=opt.UnitID)
                                            if prerequis_unit.Status is not 2:
                                                valid_enrol_units = []
                                                error_msg = 'did not pass its prerequis unit'
                                                return False
                                            elif prerequis_unit.Status is 2:
                                                credits_this_semester += credit
                                                valid_enrol_units.append(unit_id)
                                        except StudentUnit.DoesNotExist:
                                            valid_enrol_units = []
                                            error_msg = 'has not enrolled its prerequis unit before'
                                            return False
                            else:
                                credits_this_semester += credit
                                valid_enrol_units.append(unit_id)
                else:
                    credits_this_semester += credit
                    valid_enrol_units.append(unit_id)
            # Credit amount per semester musn't exceed 100
            if credits_this_semester > 100:
                valid_enrol_units = []
                error_msg = 'can not enrol units more than 100 credits a semester'
                return False

    return True
###############################################################################





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
