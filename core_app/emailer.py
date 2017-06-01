from django.core.mail import EmailMessage
from django.core.exceptions import ObjectDoesNotExist
from core_app.models import *

# Sending email to student
class SendingEmailToStudent:

    # This method is to get the message by searching all the units that are required to take in format:
    # Year <year> Semester <semester>
    #   <UnitCode> <UnitName>
    @staticmethod
    def _get_student_plan(student_id):
        student_plan = ""
        student = Student.objects.get(StudentID=student_id)
        all_studentunits = StudentUnit.objects.filter(StudentID=student)
        all_studentunits_not_passed = all_studentunits.exclude(Year=-1, Semester=-1)
        # This exception is raised when you try to email a plan but every units has been passed
        if all_studentunits_not_passed.exists() == False:
            raise ObjectDoesNotExist()
        else:
            print(all_studentunits_not_passed.exists())
            all_years = all_studentunits_not_passed.values_list('Year', flat=True).distinct()
            all_semesters = all_studentunits_not_passed.values_list('Semester', flat=True).distinct()
            for year in all_years:
                for semester in all_semesters:
                    student_plan += "\nYear {}  Semester {}\n".format(year, semester)
                    unit_ids_with_certain_year_and_semester = all_studentunits_not_passed.filter(Year=year, Semester=semester).values_list('UnitID', flat=True)
                    for id in unit_ids_with_certain_year_and_semester:
                        unit = Unit.objects.get(id=id)
                        student_plan += "\t{} {}\n".format(unit.UnitCode, unit.Name)

        return student_plan

    # This method is to setup the email and send it. The sender email has to be setup in Enrolment_Helper/settings.py
    @staticmethod
    def send_email_to_student(student_id):
        subject = 'Enrolment Plan for {}'.format(student_id)
        message = SendingEmailToStudent._get_student_plan(student_id)
        receiver = '{}@student.curtin.edu.au'.format(student_id)
        email = EmailMessage(subject, message, to=[receiver])
        email.send(fail_silently=False)

