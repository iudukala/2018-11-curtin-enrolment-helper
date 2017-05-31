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
def upload_file(request):
    """
    Handles pdf files being uploaded.
    https://docs.djangoproject.com/en/1.10/topics/http/file-uploads/
    """
    print(request)

    if request.method == 'POST':
        if request.FILES['myfile']:

            # TEMP POPULATE DATABASE!!
            populate()

            myfile = request.FILES['myfile']
            file = File(myfile)
            validator = PdfValidator(file)
            valid, output_message = validator.pdf_is_valid()
            if valid:
                information_saver = StudentInformationSaver(validator.get_validated_information())
                information_saver.set_student_units()
                # d = {'pdf_valid': 'True'}
                # HARDCODED_JSON = json.dumps(d)
                # return HttpResponse(HARDCODED_JSON, content_type='application/json')
                return HttpResponse(status=200)
            else:
                # print(validator.output_message)
                # d = {'pdf_valid': 'False'}
                # HARDCODED_JSON = json.dumps(d)
                # return HttpResponse(HARDCODED_JSON, content_type='application/json')
                return HttpResponse("Validation or saving student error.", status=500)

        else:
            return HttpResponse("ERRROR", status=403)

    else:
        return HttpResponse("Validation or saving student error.", status=403)

            # print(json.dumps(return_list))

    # d = {'Campbell': 'Front-end God'}
    # HARDCODED_JSON = json.dumps(d)
    # return HttpResponse(HARDCODED_JSON, content_type='application/json')

    # Links to Eugene's html template.
    # return render(request, 'simple_upload.html')


def get_student_list(request):
    """
    :param request:
    :return: A JSON dict object of StudentID and name
    """
    if request.method == 'GET':

        return_list = list(Student.objects.all().values('StudentID', 'Name'))

        return HttpResponse(json.dumps(return_list), content_type='application/list')


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
    return render(request, 'core_app/planner.html')
