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
            '\n\nLogged information while saving parsed information:\n---------------------------------------------\n'

    def set_student_units(self):
        if Student.objects.all().filter(StudentID=self.parsed_report['id']).exists():
            student = Student.objects.get(StudentID=self.parsed_report['id'])

        else:
            self.output_message += "Creating new student for {}\n.".format(self.parsed_report['id'])
            student = self.create_student()

        print(self.parsed_report)

        self.create_required_units(self.parsed_report['planned'])
        self.create_required_units(self.parsed_report['automatic'])
        self.create_required_units(self.parsed_report['units'])

        self.process_automatic_units(student)
        self.process_units(student)
        self.process_planned_units(student)

        # print("\nFinal database\n")
        # print(Student.objects.filter(StudentID=self.parsed_report['id']).values())
        # print("\n")
        # print(StudentUnit.objects.filter(StudentID=self.parsed_report['id']).values())

    def create_student(self):
        """
        Create a student object using the parsed PDF information.
        :return: 
        """
        self.output_message += "Creating Student {}\n".format(self.parsed_report['id'])
        s_name = self.parsed_report['name'].split(" ")
        # Removes name title.
        joined_name = " ".join(s_name[1:])
        try:
            # Create student.

            # Determine student course
            # While the object retrieved from the parer is a dict, the course information is created with
            # collections.OrderedDict() Ensuring that the first parsed course in the course Major.
            student_major_course = list(self.parsed_report['course'].items())[0][0]
            print(student_major_course)
            new_student_course = Course.objects.get(CourseID=student_major_course)

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
                "Unexpected error detected while retrieving course information: {}\n"\
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
                    UnitCode=unit_code, Credits=Decimal(unit_info['credits']), Version=unit_info['ver'], Elective=True)

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

        # print(".process_automatic_units()")
        # print(StudentUnit.objects.all().values())
        # print("--------------------------")

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

        # print("--------------------------")
        # print(".process_units()")
        # print(StudentUnit.objects.all().values())
        # print("--------------------------")

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
                prerequisites_achieved = self.determine_prerequisite(unit)

                previous_attempt = 0
                # Need previous unit attempts.
                if StudentUnit.objects.filter(StudentID=student_object, UnitID=unit).exists():
                    potential_previous_student_unit = StudentUnit.objects.filter(StudentID=student_object, UnitID=unit)
                    previous_attempt = potential_previous_student_unit.Attempts

                self.create_update_student_unit(student_object, unit, previous_attempt, unit_status,
                                                prerequisites_achieved)

            except MultipleObjectsReturned:
                self.output_message += "Multiple unit: {} detected in database.\n".format(unit_code)

                # print("--------------------------")
        # print(".process_planned_units()")
        # print(StudentUnit.objects.all().values())
        # print("--------------------------")

    def determine_prerequisite(self, unit):
        """
        Method for determining whether a planned unit has achieved its prerequisites. 
        :param unit_code, unit: 
        :return: True if prerequisite is achieved, False otherwise.
        """
        prerequisite_achieved = False

        if self.completed_units == {}:
            # Add passed units from 'units' section.
            for unitCode, unit_info in self.parsed_report['units'].items():
                if unitCode not in self.completed_units and unit_info['status'] == 'PASS':
                    self.completed_units[unit.unitCode] = unit.unit_info

            # Add all units from the 'automatic' section.
            for unitCode, unit_info in self.parsed_report['automatic'].items():
                if unitCode not in self.completed_units:
                    self.completed_units[unit.unitCode] = unit.unit_info

        if "ELECTIVE" in unit.UnitCode:
            prerequisite_achieved = True

        else:
            unit_prerequisite = Prerequisite.objects.all().filter(UnitID=unit)
            if not unit_prerequisite.exists():
                # No prerequisites exists for this unit, therefore achieves prerequisites.
                prerequisite_achieved = True

            else:
                unit_prerequisite = Prerequisite.objects.get(UnitID=unit)

        return prerequisite_achieved

    @staticmethod
    def create_update_student_unit(student_object, unit_object, attempts, status, prerequisite_achieved):

        # Check if the StudentUnit already exists within the database, creates one if it does not.
        if StudentUnit.objects.filter(StudentID=student_object, UnitID=unit_object).exists():
            student_unit_object = StudentUnit.objects.get(StudentID=student_object, UnitID=unit_object)

            student_unit_object = StudentUnit(Attempts=attempts, Status=status,
                                              PrerequisiteAchieved=prerequisite_achieved)
            student_unit_object.save()

        else:
            student_unit_object = StudentUnit(StudentID=student_object, UnitID=unit_object, Attempts=attempts,
                                              Status=status, PrerequisiteAchieved=prerequisite_achieved)
            student_unit_object.save()

    def process_elective(self, student_object, unit_code, unit_info):
        """
        HARDCODED FUNCTION!!! Relies on the database already containing the ELECTIVE1, etc units with correct fields.
        The function called if the unit is an ELECTIVE 
        :return: the ELECTIVE unit to be created for StudentUnit.
        """
        self.output_message += "ELECTIVE unit detected: {}\n".format(unit_code)
        return_unit = None

        elective_unit_version_one = Unit.objects.get(UnitCode=unit_code, Version='1',
                                                     Credits=Decimal(unit_info['credits']))
        elective_unit_version_two = Unit.objects.get(UnitCode=unit_code, Version='2',
                                                     Credits=Decimal(unit_info['credits']))
        # object, created = StudentUnit.objects.get_or_create(
        #     StudentUnit=student_object,
        #     UnitID=elective_unit_version_one
        # )
        if not StudentUnit.objects.get(StudentID=student_object, UnitID=elective_unit_version_one).exists():
            return_unit = elective_unit_version_one

        elif not StudentUnit.objects.get(StudentID=student_object, UnitID=elective_unit_version_two).exists():
            return_unit = elective_unit_version_two

        return return_unit

        # print("--------------------------")
        # print(".process_automatic_units()")
        # print(StudentUnit.objects.all().values())
        # print("--------------------------")


