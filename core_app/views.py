"""
View page. Responsible for getting data
"""
import logging
import json
# import request
# from django.shortcuts import render
from django.http import HttpResponse
from django.core import serializers
from .models import *
from .forms import UploadedFile
# from .create_student_enrolment_plan import handle_file
# from .file_validator import
# from .file_validator import upload_parsed_file

# TODO: Somewhere to store functions for parse checking.

logging.getLogger(__name__)


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
    if request.method == 'POST' or request.method == 'GET':
        # TODO: Store file.
        # FIXME: HARD CODING
        # parsed_file = UploadedFile(request.POST, request.FILES)
        upload_file = UploadedFile(request.POST, request.FILES)

        if upload_file.is_valid:
            parsed_file = upload_file(request.FILE['filename'])
            if parsed_file.is_valid:
                parsed_json = parsed_file.getJSON()

        if parsed_file.is_valid:
            parsed_json = parsed_file.getJSON()
            # NEED SOMETHING HERE TO CREATE STUDENT PLAN.
            # handle_file()
            # ACTUALLY CREATE A VALID 'template' to send to front-end.
            logging.debug("PDF form was successfully validated")
            # TODO: This actually should be the check_parsed_information stuff.

        else:
            print("FAILED")

    output = "PDF upload method: Work in progress"
    return HttpResponse(output)


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

        all_students = Student.objects.all().values('StudentID', 'Name')
        serializers_students = serializers.serialize("json", Student.objects.all(), fields=('StudentID', 'Name'))

        return HttpResponse(serializers_students, content_type='application/json')
