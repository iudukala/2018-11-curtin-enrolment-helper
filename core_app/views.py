"""
View page. Responsible for getting data
"""
import json
from django.http import HttpResponse
from django.core import serializers
from .models import *
from .enrolment_generator import Enrolment_Generator
from django.shortcuts import render
from django.core.files.storage import FileSystemStorage
from django.core.files import File
from .models import Student
from .pdf_validator import pdf_validator
from .student_information_saver import student_information_saver

# TODO: Somewhere to store functions for parse checking.


def index(request):
    """
    Default Index page
    """
    return HttpResponse("At the core_app page")


# TODO: Return 'success' (parsedInfo is Valid)
# TODO: Return 'failed' (What is required to be returned?)
def upload_file(request):
    """
    Handles pdf files being uploaded.
    https://docs.djangoproject.com/en/1.10/topics/http/file-uploads/
    """
    if request.method == 'POST' and request.FILES['myfile']:

        myfile = request.FILES['myfile']
        file = File(myfile)
        validator = pdf_validator(file)
        valid, output_message = validator.pdf_isValid()
        if valid:
            information_saver = student_information_saver(validator.get_validated_information())
            information_saver.set_student_unit()
            d = {'pdf_valid': 'True'}
            HARDCODED_JSON = json.dumps(d)
            return HttpResponse(HARDCODED_JSON, content_type='application/json')
        else:
            print(validator.output_message)
            d = {'pdf_valid': 'False'}
            HARDCODED_JSON = json.dumps(d)
            return HttpResponse(HARDCODED_JSON, content_type='application/json')

    d = {'Campbell': 'Front-end God'}
    HARDCODED_JSON = json.dumps(d)
    return HttpResponse(HARDCODED_JSON, content_type='application/json')

    # Links to Eugene's html template.
    # return render(request, 'simple_upload.html')


def get_student_list(request):
    """
    :param request:
    :return: A JSON dict object of StudentID and name
    """
    if request.method == 'GET':
        # JUST FOR TESTING
        # Can comment out once the database is up.
        # course = Course.objects.create(CourseID='311148', Version='5', Name='Course1', TotalCredits=600)
        # test_student = Student(StudentID='17080170', Name='Yoakim Persson', CreditsCompleted=550, AcademicStatus=1, CourseID=course)
        # test_student.save()

        serializers_students = serializers.serialize("json", Student.objects.all(), fields=('StudentID', 'Name'))

        return HttpResponse(serializers_students, content_type='application/json')


def generate_enrolment_plan(request):
    if request.method == 'GET':

        # recieve student ID
        e_generator = Enrolment_Generator('17080170')
        combine_JSON = e_generator.get_templates_and_plan()

    return HttpResponse(combine_JSON, content_type='application/json')
