import os
from django import test
from django.db import IntegrityError, transaction
from django.core.files import File
from core_app.models import *
from core_app.pdf_validator import PdfValidator

# Run tests with:
# 'python manage test core_app.tests'


class TestPdfValidation(test.TestCase):
    """
    Created by Yoakim Persson
    """

    @classmethod
    def setUpTestData(cls):

        database_objects = []
        cls.validators = []

        BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        test_pdf_dir = "../parser tests/test_inputs/"
        filenames_temp = \
            [
                'Darryl-pr.pdf',
                'Campbell-pr.pdf',
                # a comment by the previous group read : "# Derricks course does not exists within the database"
                # 'Derrick-pr.pdf',
                'ChienFeiLin-pr.pdf',
                'Eugene-pr.pdf',
                'XiMingWong-pr.pdf'
            ]

        cls.filenames = []
        for filename in filenames_temp:
            cls.filenames.append(os.path.join(BASE_DIR, test_pdf_dir, filename))

        """
        Yoakim's PDF.
        """
        # COURSES - Required as the Course is referenced when creating a Student object.

        Course.objects.create(CourseID='STRU-CMPSC', Name='Computer Science Stream (BSc Science)', Version=1, TotalCredits=600)
        Course.objects.create(CourseID='STRU-SWENG', Name='Software Engineering Stream (BSc Science)', Version=1, TotalCredits=600)
        Course.objects.create(CourseID='STRU-CYBSC', Name='Cyber Security Stream (BSc Science)', Version=1, TotalCredits=600)
        Course.objects.create(CourseID='STRU-INFTC', Name='Information Technology Stream (BSc Science)', Version=1, TotalCredits=600)
        Course.objects.create(CourseID='313605', Name='Software Engineering Major (BEng)', Version=1, TotalCredits=600)

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

        # Actually populates the database.
        for entry in database_objects:
            try:
                with transaction.atomic():
                    entry.save()

            except IntegrityError:
                # Object has already been created.
                pass

        for filename in cls.filenames:
            with open(filename, 'rb') as fp:
                file = File(fp)
                validator = PdfValidator(file)
                validator.read_file()
                cls.validators.append(validator)

    # PdfValidator.attributes testing.
    def test_attributes(self):
        for validator in self.validators:
            validator.is_parsed_pdf_valid = True
            validator.check_attributes()
            self.assertIs(True, validator.is_parsed_pdf_valid)

    # PdfValidator.courses testing.
    def test_courses(self):
        for validator in self.validators:
            validator.is_parsed_pdf_valid = True
            validator.check_courses()
            self.assertIs(True, validator.is_parsed_pdf_valid)

    # PdfValidator.date testing.
    def test_date(self):
        for validator in self.validators:
            validator.is_parsed_pdf_valid = True
            validator.check_date()
            self.assertIs(True, validator.is_parsed_pdf_valid)

    def test_file(self):
        """
<<<<<<< Updated upstream
        Static method so the file object still exists.
=======
>>>>>>> Stashed changes
        progress_parser (the pdf parser) closes the file object, therefore tests which are required to run the pdf
        parser again are required to create and send again.
        """
        for filename in self.filenames:
            with open(filename, 'rb') as fp:
                file = File(fp)
                validator = PdfValidator(file)

                result = validator.read_file()

            assert result is True

    def test_is_valid(self):
        """
        progress_parser (the pdf parser) closes the file object, therefore tests which are required to run the pdf
        parser again are required to create and send again.
        """
        for filename in self.filenames:
            with open(filename, 'rb') as fp:
                file = File(fp)
                validator = PdfValidator(file)

                result, output_message = validator.pdf_is_valid()

            if not result:
                print(output_message)

            assert result is True
