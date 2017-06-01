'''
Varies forms required forms within the Django Project.
'''
import datetime
import logging
import time

from django import forms
from django.core.files import File
from .progress_parser import parse_progress_report
from .models import *

# logging.getLogger(__name__)

class UploadedFileForm(forms.Form):

    '''
    The form that will hold single PDF student files.
    '''
    logging.debug("Start of UploadedFile()")
    file_name = models.CharField(max_length=255)
    parsed_file = models.FileField()

    # File parsing will be something like that. WEIRD THIS RUNS NOT WHEN 'upload_file' is called.
    # with open('/home/yoakim/2017/SEP2/SEP2_Project/PDF_PLANS/StudentProgressReport-17080170-27_Mar_2017.pdf', 'rb') as fp:
    #     parsed_file = parse_progress_report(fp)
    # fp = open(parsed_file, 'rb')

    ### THIS IS TO GENERATE A VISUAL PDF OUTPUT.
    # with open('/home/yoakim/2017/SEP2/SEP2_Project/PDF_PLANS/Yoakim_Parsed_PDF.json', 'w') as output_fp:
    #     json.dump(parsed_file, output_fp)
    # output_fp.write(str(parsed_file))
    # output_fp.close()
    # CHECKING FIELDS.
    HARDCODED_REQUIRED_JSON_FIELDS = ["course", "id", "name", "date", "units"]

    @property
    def is_valid(self):

        """
        :return: 
        """
        #Convert FileField pointer to File pointer to read
        myfile = File(fp)

        json_parsed_file = parse_progress_report(myfile)


        print(json_parsed_file)

        output_message = ''
        is_parsed_pdf_valid = True

        # DON'T THINK I CAN USE THIS AS STEAM ID WILL ALWAYS CHANGE.
        # CHECKING THAT ALL KEYS ARE CORRECT ONE.
        for key in json_parsed_file.keys():
            if key not in self.HARDCODED_REQUIRED_JSON_FIELDS:
                print("ALL KEYS ARE NOT CORRECT")
                is_parsed_pdf_valid = False
                # throw exception.

        # CHECKING THAT ALL KEYS IN THE PARSED REPORT
        for key in self.HARDCODED_REQUIRED_JSON_FIELDS:
            if key not in json_parsed_file.keys():
                print("ALL REQUIRED KEYS ARE NOT IN THE PARSED INFORMATION")
                is_parsed_pdf_valid = False

        # # Testing whether the course exists.
        for courseID, courseVersion in json_parsed_file['course'].items():
            if Course.objects.filter(CourseID=courseID, Version=courseVersion).exists():
                if True:
                    # CAN'T REMEMBER WHAT I WAS DOING HERE.
                    # NEED TO CHECK THAT THE COURSE VERSION EXISTS.
                   print("Hello")
            else:
                is_parsed_pdf_valid = False
                # FIXME: throw exception
                new_message = 'Courses: ' + str(courseID) + ', Version: ' + str(courseVersion) + ' Does not exist in the database.\n'
                output_message += new_message
                # print("No matching course found in the database")

        ###### THE UNITS DATABASE IS LIMITED TO COMPUTING UNITS.
        ###### THEREFORE CANNOT 'VALIDATE' THE AUTOMATIC UNITS.
        for unitID in json_parsed_file['units'].keys():
            if not Unit.objects.filter(UnitID=unitID).exists():
                is_parsed_pdf_valid = False
                print("Unit does not exist in the database.")

        # Testing whether the student exist.
        # # FIXME: Create student if they don't exist in database?
        if not Student.objects.filter(StudentID=json_parsed_file['id'], Name=json_parsed_file['name']).exists():
            print("Student is needed to be created")
            # TODO: Create a student as one does not exist in system.
            # student = Student(StudentID=json_parsed_file['id'], Name=json_parsed_file['name']);
            # More information required during creation.
            # student.save()

        # https://www.tutorialspoint.com/python/time_strptime.htm
        # FIXME: Most likely not the best way to implement.
        parse_date = datetime.datetime.strptime(json_parsed_file['date'], "%d %b %Y")
        current_day = datetime.datetime.strptime(time.strftime("%d %b %Y"), "%d %b %Y")

        # Check that the parsed date is older then the current date.
        if parse_date < current_day:
            new_message = "Date is invalid"
            output_message += new_message
            is_parsed_pdf_valid = False
            # print("Date is invalid")

        # print("Current date is: " + str(current_day))
        # print("Parsed data is: " + str(parse_date))

        print(output_message)

        if is_parsed_pdf_valid:
            print("ALL G, file: " + str(self.file_name) + " is valid.")
            return True

        elif not is_parsed_pdf_valid:
            print("Failed to validate: " + str(self.file_name) + ".")
            return False
