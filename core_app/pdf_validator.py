import datetime
import time

from .progress_parser import parse_progress_report
from .models import *
from django.core.exceptions import ObjectDoesNotExist


class pdf_validator():

    def __init__(self, in_filename):
        self.filename = in_filename
        self.output_message = ''
        self.json_parsed_file = {}
        self.is_parsed_pdf_valid = True
        # HARDCODED: Should be able to create these automatically.
        self.HARDCODED_REQUIRED_JSON_FIELDS = ["course", "id", "name", "date", "units", "automatic"]

    def read_file(self):
        # For dev purposed use a locally stored file.
        # with open('/home/yoakim/2017/SEP2/SEP2_Project/PDF_PLANS/StudentProgressReport-17080170-27_Mar_2017.pdf', 'rb') as fp:
        #     json_parsed_file = parse_progress_report(fp)
        # USED FOR TESTING
        try:
            with open(self.filename, 'rb') as fp:
                self.json_parsed_file = parse_progress_report(fp)

        except IOError:
            self.output_message += "File does not exist"
            self.is_parsed_pdf_valid = False
            return False

        except TypeError:
            self.output_message += "There is an issue with the file"
            self.is_parsed_pdf_valid = False
            return False

    # CHECKING THAT ALL KEYS ARE CORRECT ONE.
    def check_attributes(self):
        for key in self.json_parsed_file.keys():
            if key not in self.HARDCODED_REQUIRED_JSON_FIELDS:
                self.output_message += "All JSON attribute key are not correct"
                self.is_parsed_pdf_valid = False

        # CHECKING THAT ALL KEYS IN THE PARSED REPORT
        for key in self.HARDCODED_REQUIRED_JSON_FIELDS:
            if key not in self.json_parsed_file.keys():
                self.output_message += "All required attribute keys are not in the parsed information"
                self.is_parsed_pdf_valid = False

    def check_courses(self):
        # # Testing whether the course exists.
        for courseID, courseVersion in self.json_parsed_file['course'].items():
            if not Course.objects.filter(CourseID=courseID, Version=courseVersion).exists():
                self.is_parsed_pdf_valid = False
                new_message = 'Courses: ' + str(courseID) + ', Version: ' + str(courseVersion) + ' Does not exist in the database.\n'
                self.output_message += new_message

    def check_units(self):
        # THE UNITS DATABASE IS LIMITED TO COMPUTING UNITS.
        # THEREFORE CANNOT 'VALIDATE' THE AUTOMATIC UNITS.
        for unit_ID, unit_comp in self.json_parsed_file['units'].items():
            try:
                current_unit = Unit.objects.get(UnitID=unit_ID)
                if current_unit.Version != unit_comp['ver'] or current_unit.Credits != unit_comp['credits']:
                        self.is_parsed_pdf_valid = False
                        self.output_message += "Unit: {}, exists, however unit information appears to be incorrect.".format(unit_ID)

            except ObjectDoesNotExist:
                self.output_message += "Unit: {}, does not exist in the database".format(unit_ID)

    def check_student(self):
        # Testing whether the student exist.
        # # FIXME: Create student if they don't exist in database?
        # Remove the student's title.
        s_name = self.json_parsed_file['name'].split(' ')
        joined_name = ' '.join(s_name[1:])
        if not Student.objects.filter(StudentID=self.json_parsed_file['id'], Name=joined_name).exists():
            print("Student needs to be created")
            # TODO: Create a student as one does not exist in system.
            # student = Student(StudentID=json_parsed_file['id'], Name=json_parsed_file['name']);
            # student.save()

    def check_date(self):
        # https://www.tutorialspoint.com/python/time_strptime.htm
        # FIXME: Most likely not the best way to implement.
        parse_date = datetime.datetime.strptime(self.json_parsed_file['date'], "%d %b %Y")
        current_day = datetime.datetime.strptime(time.strftime("%d %b %Y"), "%d %b %Y")

        # Check that the parsed date is older then the current date.
        if parse_date < current_day:
            self.output_message += "Issue detected on date of the progress report"
            self.is_parsed_pdf_valid = False

    def toString_error_message(self):
        return self.output_message

    def get_is_parsed_pdf_valid(self):
        return self.is_parsed_pdf_valid

    # The function that Eugene will call to check pdf validity
    def pdf_isValid(self):
        """
        @Params: None
        @Return: Boolean: is_parsed_pdf_valid, String: output_message
        """
        # Do not run other checks if file reading fails.
        file_read_success = self.read_file()
        if file_read_success:
            self.check_attributes()
            self.check_courses()
            self.check_units()
            self.check_student()
            self.check_date()
            print(self.toString_error_message())

        if self.is_parsed_pdf_valid:
            return True

        elif not self.is_parsed_pdf_valid:
            return False, self.output_message

    # The method Eugene will can to then create and setup the student templates.
    def get_validated_information(self):
        return self.json_parsed_file
