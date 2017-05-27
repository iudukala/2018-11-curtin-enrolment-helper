from django import test
from django.db import IntegrityError, transaction
from django.core.files import File
from core_app.models import *
from core_app.pdf_validator import PdfValidator
from core_app.student_information_saver import StudentInformationSaver
import unittest


# @unittest.skip("Skipping")
class EnrolmentPlanCreationYoakim(test.TestCase):
    """
    YOAKIM'S PDF.
    """
    @classmethod
    def setUpTestData(cls):
        """
        YOAKIM'S PDF.
        :return: 
        """
        database_objects = []

        """
        Yoakim's PDF.
        """
        # COURSES - Required as the Course is referenced when creating a Student object.
        # All courses for the PDF which were used.
        cls.bachelor_of_engineering = Course.objects.create(CourseID='307808', Version='2', Name='Course1', TotalCredits=600)
        cls.bachelor_of_science = Course.objects.create(CourseID='B-SCNCE', Version='5', Name='Course1', TotalCredits=600)
        Course.objects.create(CourseID='B-SCNCE', Version='1', Name='Course1', TotalCredits=600)
        Course.objects.create(CourseID='313312', Version='1', Name='Course1', TotalCredits=600)
        Course.objects.create(CourseID='311148', Version='5', Name='Course1', TotalCredits=600)
        Course.objects.create(CourseID='BH-ENGR', Version='1', Name='Course1', TotalCredits=600)

        database_objects.append(Course(CourseID='311148',     Version='5', Name='Course1', TotalCredits=600))
        database_objects.append(Course(CourseID='MJRU-COMPT', Version='1', Name='Course2', TotalCredits=600))
        database_objects.append(Course(CourseID='313799',     Version='2', Name='Course3', TotalCredits=600))
        database_objects.append(Course(CourseID='STRU-SWENG', Version='1', Name='Course4', TotalCredits=600))

        # # Equivalence Table - Keeps track of which unit is equivalent to which unit.
        # class Equivalence(models.Model):
        #     class Meta:
        #         unique_together = (('EquivID', 'UnitID'),)
        #
        #     UnitID = models.ForeignKey(Unit, related_name='Unit', on_delete=models.CASCADE)
        #     EquivID = models.ForeignKey(Unit, related_name='EquivalentUnit', on_delete=models.CASCADE)
        #
        #
        # # Prerequisite Table - This table can be a representation of an AND's table. This table stores units to an option,
        # #                      which when getting a particular unit it will give all records of that unit which gives a set of
        # #                      options.
        # class Prerequisite(models.Model):
        #     class Meta:
        #         unique_together = (('Option', 'UnitID'),)
        #
        #     UnitID = models.ForeignKey(Unit, related_name='ThisUnit', on_delete=models.CASCADE)
        #     Option = models.IntegerField(primary_key=True)
        #
        #
        # # Options Table - This table can be a representation of an OR's table. This table stores units to an option, which when
        # #                 getting the option record will give all the units in the option.
        # class Options(models.Model):
        #     class Meta:
        #         unique_together = (('UnitID', 'Option'),)
        #
        #     UnitID = models.ForeignKey(Unit, related_name='OptUnit', on_delete=models.CASCADE)
        #     Option = models.ForeignKey(Prerequisite, related_name='Opt', on_delete=models.CASCADE)

        # Prerequisite Testing
        # COMP1000 and COMP1003
        prerequisite_unit_1 = Unit.objects.create(UnitCode='COMP1000',    Version='1', Credits=25, Semester=1)
        prerequisite_unit_2 = Unit.objects.create(UnitCode='COMP1003',    Version='1', Credits=25, Semester=1)
        unit_with_prerequisite = Unit.objects.create(UnitCode='COMP3007', Version='1', Credits=25, Semester=1)

        # Prerequisite Option is a primary integer related to a set of Units (OR relationship)
        # I believe that the Option field is unnecessary.
        prerequisite1_for_comp3007 = Prerequisite.objects.create(UnitID=unit_with_prerequisite, Option=1)
        prerequisite2_for_comp3007 = Prerequisite.objects.create(UnitID=unit_with_prerequisite, Option=2)

        option1 = Options.objects.create(UnitID=prerequisite_unit_1, Option=prerequisite1_for_comp3007)
        option2 = Options.objects.create(UnitID=prerequisite_unit_2, Option=prerequisite2_for_comp3007)

        # UNITS
        database_objects.append(Unit(UnitCode='312649',    Version='4',  Credits=25, Semester=1))
        database_objects.append(Unit(UnitCode='1920',      Version='8',  Credits=25, Semester=1))
        database_objects.append(Unit(UnitCode='CNCO2000',  Version='1',  Credits=25, Semester=1))
        database_objects.append(Unit(UnitCode='8933',      Version='11', Credits=25, Semester=1))
        database_objects.append(Unit(UnitCode='314151',    Version='1',  Credits=25, Semester=1))
        database_objects.append(Unit(UnitCode='CMPE4001',  Version='1',  Credits=25, Semester=1))
        database_objects.append(Unit(UnitCode='CMPE2002',  Version='1',  Credits=25, Semester=1))
        database_objects.append(Unit(UnitCode='10163',     Version='10', Credits=25, Semester=1))
        database_objects.append(Unit(UnitCode='ISAD4002',  Version='1',  Credits=25, Semester=1))
        database_objects.append(Unit(UnitCode='313394',    Version='3',  Credits=25, Semester=1))
        database_objects.append(Unit(UnitCode='PRJM3000',  Version='1',  Credits=25, Semester=1))
        database_objects.append(Unit(UnitCode='ISEC2001',  Version='1',  Credits=25, Semester=1))
        database_objects.append(Unit(UnitCode='314152',    Version='1',  Credits=25, Semester=1))
        database_objects.append(Unit(UnitCode='314512',    Version='1',  Credits=25, Semester=1))
        database_objects.append(Unit(UnitCode='ISAD3000',  Version='1',  Credits=25, Semester=1))
        database_objects.append(Unit(UnitCode='COMP1000',  Version='1',  Credits=25, Semester=1))
        database_objects.append(Unit(UnitCode='313392',    Version='2',  Credits=25, Semester=1))
        database_objects.append(Unit(UnitCode='313401',    Version='3',  Credits=25, Semester=1))
        database_objects.append(Unit(UnitCode='313391',    Version='3',  Credits=25, Semester=1))
        database_objects.append(Unit(UnitCode='10926',     Version='5',  Credits=25, Semester=1))
        database_objects.append(Unit(UnitCode='COMP2004',  Version='1',  Credits=25, Semester=1))
        database_objects.append(Unit(UnitCode='COMP2006',  Version='1',  Credits=25, Semester=1))
        database_objects.append(Unit(UnitCode='1922',      Version='8',  Credits=25, Semester=1))
        database_objects.append(Unit(UnitCode='4533',      Version='6',  Credits=25, Semester=1))
        database_objects.append(Unit(UnitCode='COMP3001',  Version='1',  Credits=25, Semester=1))
        database_objects.append(Unit(UnitCode='COMP3003',  Version='1',  Credits=25, Semester=1))
        database_objects.append(Unit(UnitCode='ICTE4000',  Version='1',  Credits=25, Semester=1))
        database_objects.append(Unit(UnitCode='314510',    Version='1',  Credits=25, Semester=1))
        database_objects.append(Unit(UnitCode='COMP2003',  Version='1',  Credits=25, Semester=1))

        """
        DARRYL'S PDF.
        """
        # COURSES
        database_objects.append(Course(CourseID='B-SCNCE',     Version='1', Name='Course1', TotalCredits=600))
        database_objects.append(Course(CourseID='MJRU-COMPT',  Version='1', Name='Course2', TotalCredits=600))
        database_objects.append(Course(CourseID='STRU-CMPPM',  Version='1', Name='Course3', TotalCredits=600))

        # PLANNED
        database_objects.append(Unit(UnitCode='COMP3006',  Version='1', Credits=25, Semester=1))
        database_objects.append(Unit(UnitCode='ISAD3001',  Version='2', Credits=25, Semester=1))
        database_objects.append(Unit(UnitCode='MATH1011',  Version='1', Credits=25, Semester=1))
        database_objects.append(Unit(UnitCode='COMP3007',  Version='1', Credits=25, Semester=1))
        database_objects.append(Unit(UnitCode='COMP2007',  Version='1', Credits=25, Semester=1))
        database_objects.append(Unit(UnitCode='ELECTIVE1', Version='1', Credits=25, Semester=1))
        database_objects.append(Unit(UnitCode='ELECTIVE2', Version='1', Credits=25, Semester=1))
        database_objects.append(Unit(UnitCode='ICTE3002',  Version='1', Credits=25, Semester=1))
        database_objects.append(Unit(UnitCode='ISAD3000',  Version='2', Credits=25, Semester=1))

        # AUTOMATIC
        database_objects.append(Unit(UnitCode='COMS1000', Version='2', Credits='12.5', Semester=1))

        # UNITS
        database_objects.append(Unit(UnitCode='COMP3002',  Version='1',  Credits=25, Semester=1))
        database_objects.append(Unit(UnitCode='COMP2004',  Version='1',  Credits=25, Semester=1))
        database_objects.append(Unit(UnitCode='COMP2001',  Version='1',  Credits=25, Semester=1))
        database_objects.append(Unit(UnitCode='PRJM3000',  Version='1',  Credits=25, Semester=1))
        database_objects.append(Unit(UnitCode='CNCO2000',  Version='1',  Credits=25, Semester=1))
        database_objects.append(Unit(UnitCode='STAT1002',  Version='1',  Credits=25, Semester=1))
        database_objects.append(Unit(UnitCode='ISAD1000',  Version='1',  Credits=25, Semester=1))
        database_objects.append(Unit(UnitCode='COMP3001',  Version='1',  Credits=25, Semester=1))
        database_objects.append(Unit(UnitCode='COMP2006',  Version='1',  Credits=25, Semester=1))
        database_objects.append(Unit(UnitCode='ISYS1001',  Version='1',  Credits=25, Semester=1))
        database_objects.append(Unit(UnitCode='MATH1004',  Version='1',  Credits=25, Semester=1))
        database_objects.append(Unit(UnitCode='COMP1001',  Version='1',  Credits=25, Semester=1))
        database_objects.append(Unit(UnitCode='COMP2003',  Version='1',  Credits=25, Semester=1))
        database_objects.append(Unit(UnitCode='COMP1002',  Version='1',  Credits=25, Semester=1))
        database_objects.append(Unit(UnitCode='COMP1000',  Version='1',  Credits=25, Semester=1))

        # ELECTIVES
        database_objects.append(Unit(UnitCode='ELECTIVE1',  Version='1',  Credits=12.5, Semester=-1, Elective=True))
        database_objects.append(Unit(UnitCode='ELECTIVE2',  Version='1',  Credits=12.5, Semester=-1, Elective=True))
        database_objects.append(Unit(UnitCode='ELECTIVE3',  Version='1',  Credits=12.5, Semester=-1, Elective=True))
        database_objects.append(Unit(UnitCode='ELECTIVE4',  Version='1',  Credits=12.5, Semester=-1, Elective=True))

        database_objects.append(Unit(UnitCode='ELECTIVE1',  Version='2',  Credits=12.5, Semester=-1, Elective=True))
        database_objects.append(Unit(UnitCode='ELECTIVE2',  Version='2',  Credits=12.5, Semester=-1, Elective=True))
        database_objects.append(Unit(UnitCode='ELECTIVE3',  Version='2',  Credits=12.5, Semester=-1, Elective=True))
        database_objects.append(Unit(UnitCode='ELECTIVE4',  Version='2',  Credits=12.5, Semester=-1, Elective=True))

        database_objects.append(Unit(UnitCode='ELECTIVE1',  Version='1',  Credits=25.0, Semester=-1, Elective=True))
        database_objects.append(Unit(UnitCode='ELECTIVE2',  Version='1',  Credits=25.0, Semester=-1, Elective=True))
        database_objects.append(Unit(UnitCode='ELECTIVE3',  Version='1',  Credits=25.0, Semester=-1, Elective=True))
        database_objects.append(Unit(UnitCode='ELECTIVE4',  Version='1',  Credits=25.0, Semester=-1, Elective=True))

        database_objects.append(Unit(UnitCode='ELECTIVE1',  Version='2',  Credits=25.0, Semester=-1, Elective=True))
        database_objects.append(Unit(UnitCode='ELECTIVE2',  Version='2',  Credits=25.0, Semester=-1, Elective=True))
        database_objects.append(Unit(UnitCode='ELECTIVE3',  Version='2',  Credits=25.0, Semester=-1, Elective=True))
        database_objects.append(Unit(UnitCode='ELECTIVE4',  Version='2',  Credits=25.0, Semester=-1, Elective=True))

        database_objects.append(Unit(UnitCode='ELECTIVE1',  Version='1',  Credits=50.0, Semester=-1, Elective=True))
        database_objects.append(Unit(UnitCode='ELECTIVE2',  Version='1',  Credits=50.0, Semester=-1, Elective=True))
        database_objects.append(Unit(UnitCode='ELECTIVE3',  Version='1',  Credits=50.0, Semester=-1, Elective=True))
        database_objects.append(Unit(UnitCode='ELECTIVE4',  Version='1',  Credits=50.0, Semester=-1, Elective=True))

        database_objects.append(Unit(UnitCode='ELECTIVE1',  Version='2',  Credits=50.0, Semester=-1, Elective=True))
        database_objects.append(Unit(UnitCode='ELECTIVE2',  Version='2',  Credits=50.0, Semester=-1, Elective=True))
        database_objects.append(Unit(UnitCode='ELECTIVE3',  Version='2',  Credits=50.0, Semester=-1, Elective=True))
        database_objects.append(Unit(UnitCode='ELECTIVE4',  Version='2',  Credits=50.0, Semester=-1, Elective=True))

        database_objects.append(Unit(UnitCode='ELECTIVE1',  Version='1',  Credits=75.0, Semester=-1, Elective=True))
        database_objects.append(Unit(UnitCode='ELECTIVE2',  Version='1',  Credits=75.0, Semester=-1, Elective=True))
        database_objects.append(Unit(UnitCode='ELECTIVE3',  Version='1',  Credits=75.0, Semester=-1, Elective=True))
        database_objects.append(Unit(UnitCode='ELECTIVE4',  Version='1',  Credits=75.0, Semester=-1, Elective=True))

        database_objects.append(Unit(UnitCode='ELECTIVE1',  Version='2',  Credits=75.0, Semester=-1, Elective=True))
        database_objects.append(Unit(UnitCode='ELECTIVE2',  Version='2',  Credits=75.0, Semester=-1, Elective=True))
        database_objects.append(Unit(UnitCode='ELECTIVE3',  Version='2',  Credits=75.0, Semester=-1, Elective=True))
        database_objects.append(Unit(UnitCode='ELECTIVE4',  Version='2',  Credits=50.0, Semester=-1, Elective=True))

        # STUDENTS
        database_objects.append(Student(StudentID='17080170', Name='Yoakim Sadao Persson',
                                        CreditsCompleted='300', AcademicStatus='1',
                                        CourseID=cls.bachelor_of_science))
        database_objects.append(Student(StudentID='18402636', Name='Darryl Chng',
                                        CreditsCompleted='300', AcademicStatus='1',
                                        CourseID=cls.bachelor_of_science))

        # Actually populates the database.
        for entry in database_objects:
            try:
                with transaction.atomic():
                    entry.save()

            except IntegrityError:
                # Object has already been created.
                pass

        cls.filenames = [
            '/home/yoakim/2017/SEP2/SEP2_Project/new_PDF_PLANS/Darryl-pr.pdf',
            '/home/yoakim/2017/SEP2/SEP2_Project/new_PDF_PLANS/Campbell-pr.pdf'
            # '/home/yoakim/2017/SEP2/SEP2_Project/new_PDF_PLANS/Derrick-pr.pdf',
            # '/home/yoakim/2017/SEP2/SEP2_Project/new_PDF_PLANS/ChienFeiLin-pr.pdf',
            # '/home/yoakim/2017/SEP2/SEP2_Project/new_PDF_PLANS/Eugene-pr.pdf',
            # '/home/yoakim/2017/SEP2/SEP2_Project/new_PDF_PLANS/XiMingWong-pr.pdf'
        ]

        cls.information_savers = []

        for filename in cls.filenames:
            with open(filename, 'rb') as fp:
                file = File(fp)
                validator = PdfValidator(file)
                if validator.pdf_is_valid():
                    cls.information_savers.append(StudentInformationSaver(validator.get_validated_information()))

    def test_create_student(self):
        for saver in self.information_savers:
            # Removed the created student.
            # self.student.delete()
            # self.student.StudentID = '12345678'
            saver.error_detected = False
            saver.create_student()
            print(saver.output_message)

    # def test_ensure_course_order_is_correct(self):
    #     for saver in self.information_savers:
    #         student_major = list(saver.parsed_report['course'].items())[0][0]
    #         print(saver.output_message)
    #         self.assertTrue(student_major == self.bachelor_of_science.CourseID)

    def test_set_student_units(self):
        for saver in self.information_savers:
            saver.error_detected = False
            saver.set_student_units()
            print(saver.output_message)
            self.assertIs(False, saver.error_detected)