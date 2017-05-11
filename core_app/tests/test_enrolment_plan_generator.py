from django.test import TestCase
from django.core.files import File
# from core_app.models import *
from core_app.models import Student
from core_app.models import Course
from core_app.models import Unit
from core_app.pdf_validator import pdf_validator
from core_app.student_information_saver import student_information_saver
from core_app.enrolment_generator import Enrolment_Generator
import unittest


@unittest.skip("Skipping")
class test_enrolment_plan_creation(TestCase):
    @classmethod
    def setUpTestData(cls):
        # COURSES
        cls.course1 = Course.objects.create(CourseID='311148',      Version='5', Name='Course1', TotalCredits=600)
        cls.course2 = Course.objects.create(CourseID='MJRU-COMPT',  Version='1', Name='Course2', TotalCredits=600)
        cls.course3 = Course.objects.create(CourseID='313799',      Version='2', Name='Course3', TotalCredits=600)
        cls.course4 = Course.objects.create(CourseID='STRU-SWENG',  Version='1', Name='Course4', TotalCredits=600)

        # STUDENT
        cls.student = Student.objects.create(StudentID='17080170', Name='Yoakim Sadao Persson', CreditsCompleted='300', AcademicStatus='1', CourseID=cls.course1)

        # UNITS
        cls.unit1 = Unit.objects.create(UnitID='312649',    Version='4',  Credits=12.5, Semester=1)
        cls.unit1 = Unit.objects.create(UnitID='1920',      Version='8',  Credits=12.5, Semester=1)
        cls.unit1 = Unit.objects.create(UnitID='CNCO2000',  Version='1',  Credits=12.5, Semester=1)
        cls.unit1 = Unit.objects.create(UnitID='8933',      Version='11', Credits=12.5, Semester=1)
        cls.unit1 = Unit.objects.create(UnitID='314151',    Version='1',  Credits=12.5, Semester=1)
        cls.unit1 = Unit.objects.create(UnitID='CMPE4001',  Version='1',  Credits=12.5, Semester=1)
        cls.unit1 = Unit.objects.create(UnitID='CMPE2002',  Version='10', Credits=12.5, Semester=1)
        cls.unit1 = Unit.objects.create(UnitID='10163',     Version='1',  Credits=12.5, Semester=1)
        cls.unit1 = Unit.objects.create(UnitID='ISAD4002',  Version='3',  Credits=12.5, Semester=1)
        cls.unit1 = Unit.objects.create(UnitID='313394',    Version='1',  Credits=12.5, Semester=1)
        cls.unit1 = Unit.objects.create(UnitID='PRJM3000',  Version='1',  Credits=12.5, Semester=1)
        cls.unit1 = Unit.objects.create(UnitID='ISEC2001',  Version='1',  Credits=12.5, Semester=1)
        cls.unit1 = Unit.objects.create(UnitID='314152',    Version='1',  Credits=12.5, Semester=1)
        cls.unit1 = Unit.objects.create(UnitID='314512',    Version='1',  Credits=12.5, Semester=1)
        cls.unit1 = Unit.objects.create(UnitID='ISAD3000',  Version='1',  Credits=12.5, Semester=1)
        cls.unit1 = Unit.objects.create(UnitID='COMP1000',  Version='1',  Credits=12.5, Semester=1)
        cls.unit1 = Unit.objects.create(UnitID='313392',    Version='2',  Credits=12.5, Semester=1)
        cls.unit1 = Unit.objects.create(UnitID='313401',    Version='3',  Credits=12.5, Semester=1)
        cls.unit1 = Unit.objects.create(UnitID='313391',    Version='3',  Credits=12.5, Semester=1)
        cls.unit1 = Unit.objects.create(UnitID='10926',     Version='5',  Credits=12.5, Semester=1)
        cls.unit1 = Unit.objects.create(UnitID='COMP2004',  Version='1',  Credits=12.5, Semester=1)
        cls.unit1 = Unit.objects.create(UnitID='COMP2006',  Version='1',  Credits=12.5, Semester=1)
        cls.unit1 = Unit.objects.create(UnitID='1922',      Version='8',  Credits=12.5, Semester=1)
        cls.unit1 = Unit.objects.create(UnitID='4533',      Version='6',  Credits=12.5, Semester=1)
        cls.unit1 = Unit.objects.create(UnitID='COMP3001',  Version='1',  Credits=12.5, Semester=1)
        cls.unit1 = Unit.objects.create(UnitID='COMP3003',  Version='1',  Credits=12.5, Semester=1)
        cls.unit1 = Unit.objects.create(UnitID='ICTE4000',  Version='1',  Credits=12.5, Semester=1)
        cls.unit1 = Unit.objects.create(UnitID='314510',    Version='1',  Credits=12.5, Semester=1)
        cls.unit1 = Unit.objects.create(UnitID='COMP2003',  Version='1',  Credits=12.5, Semester=1)

        filename = '/home/yoakim/2017/SEP2/SEP2_Project/PDF_PLANS/StudentProgressReport-17080170-27_Mar_2017.pdf'

        fp = open(filename, 'rb')
        file = File(fp)

        cls.validator = pdf_validator(file)
        valid, _ = cls.validator.pdf_isValid()
        if valid:
            cls.information_saver = student_information_saver(cls.validator.get_validated_information())
            cls.information_saver.set_student_unit()
            cls.plan_generator = Enrolment_Generator('17080170')

            print(cls.validator.get_validated_information())
        else:
            print("SHOULD NOT FAIL HERE")

        file.close()
        fp.close()

    def test_get_templates_and_plans(self):
        self.plan_generator.get_templates_and_plan()
