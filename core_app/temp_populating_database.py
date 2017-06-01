from core_app.models import *
from django.db import IntegrityError, transaction


def delete_database():
    # all_units = unit.objects.all().delete()
    Unit.objects.all().delete()
    # for entry in all_units:
    #     entry.delete()

    all_courses = Course.objects.all().delete()
    # for entry in all_courses:
    #     entry.delete()

    all_students = Student.objects.all().delete()
    # for entry in all_students:
    #     entry.delete()

    all_studentunits = StudentUnit.objects.all().delete()
    # for entry in all_studentunits:
    #     entry.delete()

    all_prerequisistes = Prerequisite.objects.all().delete()
    # for entry in all_prerequisistes:
    #     entry.delete()

    all_options = Options.objects.all().delete()
    # for entry in all_options:
    #     entry.delete()


def populate():
    database_objects = []

    # COURSES - Required as the Course is referenced when creating a Student object.
    # All courses for the PDF which were used.
    # bachelor_of_engineering = Course.objects.create(CourseID='307808', Version='2', Name='Course1', TotalCredits=600)
    # bachelor_of_science = Course.objects.create(CourseID='B-SCNCE', Version='5', Name='Course1', TotalCredits=600)

    database_objects.append(Course(CourseID='307808', Version='2', Name='Course1', TotalCredits=600))
    database_objects.append(Course(CourseID='B-SCNCE', Version='1', Name='Course1', TotalCredits=600))
    database_objects.append(Course(CourseID='B-SCNCE', Version='5', Name='Course1', TotalCredits=600))
    database_objects.append(Course(CourseID='313312', Version='1', Name='Course1', TotalCredits=600))
    database_objects.append(Course(CourseID='311148', Version='5', Name='Course1', TotalCredits=600))
    database_objects.append(Course(CourseID='BH-ENGR', Version='1', Name='Course1', TotalCredits=600))
    database_objects.append(Course(CourseID='313605', Version='1', Name='Software Engineering Major (BEng)',
                                   TotalCredits=600))

    database_objects.append(Course(CourseID='311148',     Version='5', Name='Course1', TotalCredits=600))
    database_objects.append(Course(CourseID='MJRU-COMPT', Version='1', Name='Course2', TotalCredits=600))
    database_objects.append(Course(CourseID='313799',     Version='2', Name='Course3', TotalCredits=600))
    database_objects.append(Course(CourseID='STRU-SWENG', Version='1', Name='Course4', TotalCredits=600))

    # Prerequisite Testing
    # COMP1000 and COMP1003
    # prerequisite_unit_1 = Unit.objects.create(UnitCode='COMP1000',    Version='1', Credits=25, Semester=1)
    # prerequisite_unit_2 = Unit.objects.create(UnitCode='COMP1003',    Version='1', Credits=25, Semester=1)
    # unit_with_prerequisite = Unit.objects.create(UnitCode='COMP3007', Version='1', Credits=25, Semester=1)

    # Prerequisite Option is a primary integer related to a set of Units (OR relationship)
    # I believe that the Option field is unnecessary.
    # prerequisite1_for_comp3007 = Prerequisite.objects.create(UnitID=unit_with_prerequisite, Option=1)
    # prerequisite2_for_comp3007 = Prerequisite.objects.create(UnitID=unit_with_prerequisite, Option=2)

    # option1 = Options.objects.create(UnitID=prerequisite_unit_1, Option=prerequisite1_for_comp3007)
    # option2 = Options.objects.create(UnitID=prerequisite_unit_2, Option=prerequisite2_for_comp3007)

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
