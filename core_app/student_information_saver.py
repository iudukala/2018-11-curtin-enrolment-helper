from .models import *
from decimal import Decimal
from django.core.exceptions import ObjectDoesNotExist, MultipleObjectsReturned
"""
Basic steps:
    determine all the units that the student is required to do.
        Based on the courses
"""


class StudentInformationSaver:
    """
    Check Prerequisite and Equivalence. 
    """

    def __init__(self, in_json_parsed_file):
        self.parsed_report = in_json_parsed_file
        self.completed_units = {}
        self.error_detected = False
        self.output_message = \
            '\n\nLogged information while saving parsed information:\n---------------------------------------------\n' \
            'Student: {}, {}\n'.format(self.parsed_report['id'], self.parsed_report['name'])

    def set_student_units(self):
        if Student.objects.all().filter(StudentID=self.parsed_report['id']).exists():
            this_student = Student.objects.get(StudentID=self.parsed_report['id'])

        else:
            self.output_message += "Creating new student for {}\n.".format(self.parsed_report['id'])
            this_student = self.create_student()

        self.create_required_units(self.parsed_report['planned'])
        self.create_required_units(self.parsed_report['automatic'])
        self.create_required_units(self.parsed_report['units'])

        self.process_automatic_units(this_student)
        self.process_units(this_student)
        self.process_planned_units(this_student)

    def create_student(self):
        """
        Create a student object using the parsed PDF information.
        :return: 
        """
        s_name = self.parsed_report['name'].split(" ")
        # Removes name title.
        joined_name = " ".join(s_name[1:])
        try:
            # Create student.

            # Determine student course
            # While the object retrieved from the parer is a dict, the course information is created with
            # collections.OrderedDict() Ensuring that the first parsed course in the course Major.
            student_major_course_info = list(self.parsed_report['course'].items())[0]
            new_student_course = Course.objects.get(CourseID=student_major_course_info[0],
                                                    Version=student_major_course_info[1])

            # Determine completed credits, and set completed units.
            completed_credits, self.completed_units = self.calculate_completed_credits()

            # Determine academic status.
            # FIXME: Calculate academic status?
            default_academic_status = 1

            new_student = Student(StudentID=self.parsed_report['id'], Name=joined_name,
                                  AcademicStatus=default_academic_status, CourseID=new_student_course,
                                  CreditsCompleted=completed_credits)
            self.output_message += "New student with id: {} created.\n".format(new_student.StudentID)
            # FIXME: Actually save student.
            new_student.save()

        except ObjectDoesNotExist:
            self.error_detected = True
            self.output_message += \
                "Unexpected error while creating student detected retrieving course information: {}\n"\
                .format(self.parsed_report['course'][0])

        return Student.objects.get(StudentID=self.parsed_report['id'])

    def calculate_completed_credits(self):
        """
        Calculates the number of credits completed by the student from the parsed plan.
        :return: Number of credits, as well as a dict containing completed units.
        """
        # FIXME:
        counted_credits = 0
        completed_units = {}

        # Should cover units.
        for unitCode, unit_info in self.parsed_report['units'].items():
            if unitCode not in completed_units and unit_info['status'] == 'PASS':
                completed_units[unitCode] = unit_info
                counted_credits += Decimal(unit_info['credits'])

        # Credited units.
        for unitCode, unit_info in self.parsed_report['automatic'].items():
            if unitCode not in completed_units:
                completed_units[unitCode] = unit_info
                counted_credits += Decimal(unit_info['credits'])

        return counted_credits, completed_units

    def create_required_units(self, student_dict):
        """
        Function checks whether units exist within 'planned', 'automatic' and 'units'
        Creates them as Electives if they do not exist.
        :return: 
        """
        # THE UNITS DATABASE IS LIMITED TO COMPUTING UNITS.
        # PLANNED
        for unit_code, unit_info in student_dict.items():

            # For electives. - Currently hard coding electives.
            if "ELECTIVE" in unit_code:
                pass

            elif not Unit.objects.all().filter(
                    UnitCode=unit_code, Credits=Decimal(unit_info['credits']), Version=unit_info['ver']).exists():
                # Create a new unit.
                # Potentially an elective OR typo.
                self.output_message += "Creating new unit: {}, Version: {}, Credits: {}.\n"\
                    .format(unit_code,  unit_info['ver'], unit_info['credits'])

                Unit.objects.create(
                    UnitCode=unit_code, Credits=Decimal(unit_info['credits']), Version=unit_info['ver'], Elective=True,
                    Semester=3)

    def process_automatic_units(self, student_object):
        """
        Can assume that the prerequisite for these units have been met.
        As these are units that have been completed, status is passed (2)
        Only single attempt is recorded.
        :param student_object: 
        :return: 
        """

        # Assumptions
        prerequisite_achieved = True
        unit_status = 2
        attempt = 1

        for unit_code, unit_info in self.parsed_report['automatic'].items():

            try:
                if "ELECTIVE" in unit_code:
                    unit = self.process_elective(student_object, unit_code, unit_info)

                else:
                    unit = Unit.objects.get(UnitCode=unit_code, Credits=Decimal(unit_info['credits']), Version=unit_info['ver'])

                self.create_update_student_unit(student_object, unit, attempt, unit_status, prerequisite_achieved)

            except MultipleObjectsReturned:
                self.output_message += "Multiple unit: {} detected in database.\n".format(unit_code)

    def process_units(self, student_object):
        """
        Method used to process all regular units with parsed PDF.
        Can assume that the prerequisite for these units have been met.
        :param student_object: 
        :return: 
        """
        # Assumptions
        prerequisite_achieved = True

        for unit_code, unit_info in self.parsed_report['units'].items():

            try:
                if "ELECTIVE" in unit_code:
                    unit = self.process_elective(student_object, unit_code, unit_info)

                else:
                    unit = Unit.objects.get(UnitCode=unit_code, Credits=Decimal(unit_info['credits']),
                                            Version=unit_info['ver'])

                if unit_info['status'] == 'FAIL' or unit_info['status'] == 'WD':
                    unit_status = 3

                elif unit_info['status'] == 'ENR':
                    unit_status = 1

                else:
                    unit_status = 2

                self.create_update_student_unit(student_object, unit, unit_info['attempt'], unit_status,
                                                prerequisite_achieved)

            except MultipleObjectsReturned:
                self.output_message += "Multiple unit: {} detected in database.\n".format(unit_code)

    def process_planned_units(self, student_object):
        """
        Cannot assume that prerequisites have been met form these units.
        These units could be new attempts of previously done units.
        As these are planned units, the status for them all is 'Not Done' (1)
        :param student_object: 
        :return: 
        """

        # Assumptions
        unit_status = 1

        for unit_code, unit_info in self.parsed_report['planned'].items():

            try:
                if "ELECTIVE" in unit_code:
                    unit = self.process_elective(student_object, unit_code, unit_info)

                else:
                    unit = Unit.objects.get(UnitCode=unit_code, Credits=Decimal(unit_info['credits']),
                                            Version=unit_info['ver'])

                # UNTIL_WORKED_OUT_ELECTIVES.
                prerequisites_achieved = self.determine_prerequisite(student_object, unit)

                previous_attempt = 0
                # Need previous unit attempts.
                if StudentUnit.objects.filter(StudentID=student_object, UnitID=unit).exists():
                    potential_previous_student_unit = StudentUnit.objects.get(StudentID=student_object, UnitID=unit)
                    previous_attempt = potential_previous_student_unit.Attempts

                self.create_update_student_unit(student_object, unit, previous_attempt, unit_status,
                                                prerequisites_achieved)

            except MultipleObjectsReturned:
                self.output_message += "Multiple unit: {} detected in database.\n".format(unit_code)

    def determine_prerequisite(self, student_object, unit):
        """

        :param student_object:
        :param unit:
        :return:
        """
        prerequisite_achieved = True

        # No need to process electives.
        if "ELECTIVE" in unit.UnitCode:
            pass

        else:
            #     # COMP3007 - Machine Percpective. Version: 1, Credit: 25
            #     # Requires - COMP1002 Version: 1, Credit: 25
            #     #            COMP1000 Version: 1, Credit: 25
            #     # unit = Unit.objects.get(UnitCode='COMP3007', Version='1', Credits=25)
            #
            #     # Visual idea
            #     #    Prerequisite   Options
            #     #         OR         AND         OR
            #     # (unitid or unitid) and (unitid or unit)

            prerequisite_list = Prerequisite.objects.filter(UnitID=unit)

            # Loop though prerequisites.
            for prerequisite_object in prerequisite_list:

                # if Options.objects.filter(Option=Options.objects.get(unit_and_list.Option)).exists():
                if Options.objects.filter(Option=prerequisite_object).exists():
                    or_achieved = False
                    # Should contain the Options available
                    option_list = Options.objects.filter(Option=prerequisite_object)

                    for option_object in option_list:
                        print("{}".format(option_object.UnitID.UnitCode))
                        if StudentUnit.objects.filter(StudentID=student_object, UnitID=option_object.UnitID).exists():
                            student_unit = StudentUnit.objects.get(StudentID=student_object,
                                                                   UnitID=option_object.UnitID)
                            if student_unit.Status == '2':
                                or_achieved = True
                                continue
                                # # If the student has passed no need to check the other 'OR' units.
                                # if student_unit.Status == '2':
                                #     or_achieved = True
                                #     continue

                    # if or_achieved is false here the prerequisite have not been met.
                    if not or_achieved:
                        prerequisite_achieved = False
                        continue

        return prerequisite_achieved

    @staticmethod
    def create_update_student_unit(student_object, unit_object, attempts, status, prerequisite_achieved):

        # Check if the StudentUnit already exists within the database, creates one if it does not.
        if StudentUnit.objects.filter(StudentID=student_object, UnitID=unit_object).exists():
            existing_student_unit_object = StudentUnit.objects.get(StudentID=student_object, UnitID=unit_object)

            existing_student_unit_object.Attempts = attempts
            existing_student_unit_object.Status = status
            existing_student_unit_object.PrerequisiteAchieved = prerequisite_achieved

            existing_student_unit_object.save()

        else:
            student_unit_object = StudentUnit(StudentID=student_object, UnitID=unit_object, Attempts=attempts,
                                              Status=status, PrerequisiteAchieved=prerequisite_achieved)
            student_unit_object.save()

    @staticmethod
    def process_elective(student_object, unit_code, unit_info):
        """
        HARDCODED FUNCTION!!! Relies on the database already containing the ELECTIVE1, etc units with correct fields.
        The function called if the unit is an ELECTIVE 
        :return: the ELECTIVE unit to be created for StudentUnit.
        """
        # self.output_message += "ELECTIVE unit detected: {}\n".format(unit_code)
        return_unit = None

        elective_unit_version_one = Unit.objects.get(UnitCode=unit_code, Version='1',
                                                     Credits=Decimal(unit_info['credits']))
        elective_unit_version_two = Unit.objects.get(UnitCode=unit_code, Version='2',
                                                     Credits=Decimal(unit_info['credits']))

        if not StudentUnit.objects.filter(StudentID=student_object, UnitID=elective_unit_version_one).exists():
            return_unit = elective_unit_version_one

        elif not StudentUnit.objects.filter(StudentID=student_object, UnitID=elective_unit_version_two).exists():
            return_unit = elective_unit_version_two

        return return_unit

