import datetime

from .progress_parser import parse_progress_report
from .models import *
from django.core.exceptions import ObjectDoesNotExist


class PdfValidator:

    def __init__(self, file):
        self.in_file = file
        self.output_message = \
            '\n\nIssue detected during pdf validation:\n---------------------------------------------\n'
        self.json_parsed_file = {}
        self.is_parsed_pdf_valid = True
        # HARDCODED: Should be able to create these automatically.
        self.HARDCODED_REQUIRED_JSON_FIELDS = ["course", "id", "name", "date", "units", "automatic", "planned"]

    def read_file(self):
        """
        Reads the file provided in the constructor and attempts to parse the progress report.
        :return: True if parsing was successful, False if not.
        """
        try:
            self.json_parsed_file = parse_progress_report(self.in_file)
            self.output_message += 'Student: {}, {}\n'.format(self.json_parsed_file['id'],
                                                              self.json_parsed_file['name'])
            return True

        except IOError:
            self.output_message += "File does not exist\n"
            self.is_parsed_pdf_valid = False
            return False

        except TypeError:
            self.output_message += "There is an issue with the file\n"
            self.is_parsed_pdf_valid = False
            return False

    # The function that Eugene will call to check pdf validity
    def pdf_is_valid(self):
        """
        Function that runs all the validators on the parsed PDF file.
        :return:
        """
        # Do not run other checks if file reading fails.
        if self.read_file():
            self.check_attributes()
            self.check_courses()
            self.check_date()

        return self.is_parsed_pdf_valid, self.output_message

    # The method Eugene will can to then create and setup the student templates.
    def get_validated_information(self):
        return self.json_parsed_file

    # CHECKING THAT ALL KEYS ARE CORRECT ONE.
    def check_attributes(self):
        for key in self.json_parsed_file.keys():
            if key not in self.HARDCODED_REQUIRED_JSON_FIELDS:
                print(key)
                self.output_message += "All JSON attribute key are not correct\n"
                self.is_parsed_pdf_valid = False

        # CHECKING THAT ALL KEYS IN THE PARSED REPORT
        for key in self.HARDCODED_REQUIRED_JSON_FIELDS:
            if key not in self.json_parsed_file.keys():
                self.output_message += "All required attribute keys are not in the parsed information\n"
                self.is_parsed_pdf_valid = False

    def check_courses(self):
        """
        Check that the major course for the student exists within the database.
        :return:
        """
        course_id = list(self.json_parsed_file['course'].items())[0][0]
        version = list(self.json_parsed_file['course'].items())[0][1]
        if not Course.objects.filter(CourseID=course_id, Version=version).exists():
            self.is_parsed_pdf_valid = False
            new_message = 'Courses: ' + str(course_id) + ', Version: ' + str(version) + \
                          ' Does not exist in the database.\n'
            self.output_message += new_message

    def check_date(self):
        """
        Checks that the date in the parsed report is valid. (in the past).
        :return:
        """
        parse_date = datetime.datetime.strptime(self.json_parsed_file['date'], "%d %b %Y")
        current_day = datetime.datetime.now()

        # Check that the parsed date is older then the current date.
        if parse_date > current_day:
            self.output_message += "Issue detected on date of the progress report. Parsed date: {}\n".format(parse_date)
            self.is_parsed_pdf_valid = False

    def to_string_error_message(self):
        return self.output_message

    def get_is_parsed_pdf_valid(self):
        return self.is_parsed_pdf_valid
