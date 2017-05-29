from django.http import HttpResponse
from django.core import serializers
from django.shortcuts import render
from django.core.files import File
from .models import Student

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
    if request.method == 'POST' and request.FILES['myfile']:

        # TEMP POPULATE DATABASE!!
        populate()

        myfile = request.FILES['myfile']
        file = File(myfile)
        validator = PdfValidator(file)
        valid, output_message = validator.pdf_is_valid()
        if valid:
            information_saver = StudentInformationSaver(validator.get_validated_information())
            information_saver.set_student_units()
            d = {'pdf_valid': 'True'}
            HARDCODED_JSON = json.dumps(d)
            return HttpResponse(HARDCODED_JSON, content_type='application/json')
        else:
            print(validator.output_message)
            d = {'pdf_valid': 'False'}
            HARDCODED_JSON = json.dumps(d)
            return HttpResponse(HARDCODED_JSON, content_type='application/json')

    # d = {'Campbell': 'Front-end God'}
    # HARDCODED_JSON = json.dumps(d)
    # return HttpResponse(HARDCODED_JSON, content_type='application/json')

    # Links to Eugene's html template.
    return render(request, 'simple_upload.html')


def get_student_list(request):
    """
    :param request:
    :return: A JSON dict object of StudentID and name
    """
    if request.method == 'GET':

        serializers_students = serializers.serialize("json", Student.objects.all(), fields=('StudentID', 'Name'))

        return HttpResponse(serializers_students, content_type='application/json')
