from .models import *
from .models import Course
from .models import Student
from .models import Unit
from .models import CourseTemplate
from .models import Credential
from .models import StudentUnit
from django.core.exceptions import ObjectDoesNotExist
# from .progress_parser import parse_progress_report
# from .pdf_validator import pdf_validator
"""
Basic steps:
    determine all the units that the student is required to do.
        Based on the courses
"""
#####
# {
#     template: {
#         <YEAR> : {
#         <SEMESTER> : {
#             <UNIT ID> : { name: <NAME>, credits: <CREDIT WORTH> }
#             }
#         }
#     }
#     plan: {
#         <YEAR> : {
#             <SEMESTER> : {
#                 <UNIT ID> : {
#                          name: <NAME>, credits: <CREDIT WORTH>, attempts: <PREV. ATTEMPTS>
#                 }
#             }
#         }
#     }
# }


class student_information_saver():

    def __init__(self, in_json_parsed_file):
        self.parsed_report = in_json_parsed_file

    def set_student_unit(self):
        student = Student.objects.get(StudentID=self.parsed_report['id'])
        for unitID, unit_info in self.parsed_report['units'].items():
            try:
                unit = Unit.objects.get(UnitID=unitID)
                if unit_info['status'] == 'FAIL' or unit_info['status'] == 'WD':
                    unit_status = False
                else:
                    unit_status = True
                new_student_unit = StudentUnit(StudentID=student, UnitID=unit, Attempts=unit_info['attempt'], Status=unit_status)
                new_student_unit.save()

            # Unit can be elective.
            except ObjectDoesNotExist:
                print("AN ELECTIVE!!")


def determine_unit_progress(unit_set):
    '''
    attempt_dict = {
        id: <>
        info: {
            status: <>
            attempts: <>
        }
    }
    @Params: All units student has done.
    @Return: a dict object, with unit as key and number of attempts as value.
    '''
