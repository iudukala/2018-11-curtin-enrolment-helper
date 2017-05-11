"""
View page. Responsible for getting data
"""
import logging
import json
# import request
# from django.shortcuts import render
from django.http import HttpResponse
from django.core import serializers
from django.shortcuts import render
from django.core.files.storage import FileSystemStorage
from django.core.files import File
from .models import Student
from .forms import UploadedFileForm

# from .file_validator import
# from .file_validator import upload_parsed_file

# TODO: Somewhere to store functions for parse checking.

logging.getLogger(__name__)

def index(request):
    """
    Default Index page
    """
    print(__name__)
    logging.debug('index page')
    print(request)
    return HttpResponse("At the core_app page")

def test_view(request):
    # TODO: Write something useful.
    """
    """
    logging.debug('test_view page')
    output = "TESTING OUTPUT"
    return HttpResponse(json.dumps(output))
    # return HttpResponse(json.dumps({'key': 'value'}), mimeType="application/json")


# TODO: Return 'success' (parsedInfo is Valid)
# TODO: Return 'failed' (What is required to be returned?)
def upload_file(request):
    """
    Handles pdf files being uploaded.
    https://docs.djangoproject.com/en/1.10/topics/http/file-uploads/
    """
    if request.method == 'POST' and request.FILES['myfile']:
        # TODO: Store file.
        # FIXME: HARD CODING

        myfile = request.FILES['myfile']
        file = File(myfile)
        fs = FileSystemStorage()
        output = file.readline()
        uploaded_file_url = fs.url(output)
        return render(request, 'simple_upload.html', {'uploaded_file_url': uploaded_file_url })

        #parsed_file = UploadedFile(request.POST, request.FILES)
        #form = UploadedFileForm(request.POST, request.FILES)
        #if form.is_valid(form.parsed_file):
        #    form.parsed_file.save()
        #    parsed_json = parsed_file.getJSON()


        # if upload_file.is_valid:
        #     parsed_file = upload_file(request.FILE['filename'])
        #     if parsed_file.is_valid:
        #         parsed_json = parsed_file.getJSON()

        # if parsed_file.is_valid:
        #     parsed_json = parsed_file.getJSON()
        #     # NEED SOMETHING HERE TO CREATE STUDENT PLAN.
        #    # handle_file()
        #     # ACTUALLY CREATE A VALID 'template' to send to front-end.
        #     logging.debug("PDF form was successfully validated")
        #     # TODO: This actually should be the check_parsed_information stuff.
        #
        # else:
        #     print("FAILED")

    # output = "PDF upload method: Work in progress"
    # return HttpResponse(output)
    return render(request, 'simple_upload.html')

def get_student_list(request):
    """
    :param request: 
    :return: A JSON dict object of StudentID and name
    """
    logging.debug("Start get_student_list")
    # TODO: Need to return all Student names & IDs as a dictionary.
    # if request.method == 'POST':
    all_students = Student.objects.all().values('StudentID', 'Name')
    serializers_students = serializers.serialize("json", all_students)
    print(json.dumps(serializers_students))

    return HttpResponse(json.dumps(json.dumps(serializers_students)), content_type='application/json')
    # return HttpResponse('get_student_list')
