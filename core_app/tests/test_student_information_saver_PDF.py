import os
from django import test
from django.db import IntegrityError, transaction
from django.core.files import File
from core_app.models import *
from core_app.pdf_validator import PdfValidator
from core_app.student_information_saver import StudentInformationSaver


class TestEnrolmentPlanCreation(test.TestCase):
    """
    Created by Yoakim Persson
    """

    def save_entry(data):
        for entry in data:
            try:
                with transaction.atomic():
                    entry.save()

            except IntegrityError:
                # Object has already been created
                pass

    @classmethod
    def setUpTestData(cls):

        BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        test_pdf_dir = "../parser tests/test_inputs/"

        database_objects = []
        cls.information_savers = []

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


        # Populating test data with data from Eugene's populate_db.py
        units = []
        prerequisites = []
        options = []
        equivalences = []
        courses = []
        course_templates = []
        course_template_options = []

        # Data from Eugene's populate database.
        units.append(Unit(UnitCode='COMP1001', Name='Object Oriented Program Design', Version=1, Semester=3, Credits=25, Elective=False))

        units.append(Unit(UnitCode='IASD1000', Name='Introduction to Software Engineering', Version=1, Semester=1, Credits=25, Elective=False))

        units.append(Unit(UnitCode='COMS1000', Name='Science Communications', Version=1, Semester=3, Credits=12.5, Elective=False))

        units.append(Unit(UnitCode='STAT1002', Name='Statistical Data Analysis', Version=1, Semester=3, Credits=12.5, Elective=False))

        units.append(Unit(UnitCode='MATH1015', Name='Linear Algebra 1', Version=1, Semester=3, Credits=25, Elective=False))

        units.append(Unit(UnitCode='COMP1002', Name='Data Structures and Algorithms', Version=1, Semester=3, Credits=25, Elective=False))

        units.append(Unit(UnitCode='COMP1000', Name='Unix and C Programming', Version=1, Semester=2, Credits=25, Elective=False))

        units.append(Unit(UnitCode='ISYS1001', Name='Database Systems', Version=1, Semester=2, Credits=25, Elective=False))

        units.append(Unit(UnitCode='COMP1006', Name='Foundations of Computer Science', Version=1, Semester=2, Credits=25, Elective=False))

        units.append(Unit(UnitCode='CNCO2000', Name='Computer Communications', Version=1, Semester=1, Credits=25, Elective=False))

        units.append(Unit(UnitCode='COMP2006', Name='Operating Systems', Version=1, Semester=1, Credits=25, Elective=False))

        units.append(Unit(UnitCode='COMP2003', Name='Object Oriented Software Engineering', Version=1, Semester=1, Credits=25, Elective=False))

        units.append(Unit(UnitCode='MATH1011', Name='Calculus 1', Version=1, Semester=3, Credits=25, Elective=False))

        units.append(Unit(UnitCode='COMP3001', Name='Design and Analysis of Algorithms', Version=1, Semester=1, Credits=25, Elective=False))

        units.append(Unit(UnitCode='ISEC2001', Name='Fundamental Concepts of Data Security', Version=2, Semester=1, Credits=25, Elective=False))

        units.append(Unit(UnitCode='ISEC2000', Name='Fundamental Concepts of Cryptography', Version=1, Semester=1, Credits=25, Elective=False))

        units.append(Unit(UnitCode='COMP2002', Name='Unix Systems Programming', Version=1, Semester=1, Credits=25, Elective=False))

        units.append(Unit(UnitCode='COMP2004', Name='Computer Graphics', Version=1, Semester=3, Credits=25, Elective=False))

        units.append(Unit(UnitCode='COMP2008', Name='Mobile Application Development', Version=1, Semester=2, Credits=25, Elective=False))

        units.append(Unit(UnitCode='COMP2007', Name='Programming Languages', Version=1, Semester=2, Credits=25, Elective=False))

        units.append(Unit(UnitCode='CMPE2002', Name='Requirements Engineering', Version=1, Semester=2, Credits=25, Elective=False))

        units.append(Unit(UnitCode='ISEC3002', Name='Penetration Testing and Defence', Version=1, Semester=2, Credits=25, Elective=False))

        units.append(Unit(UnitCode='COMP2005', Name='Computing Topics', Version=1, Semester=2, Credits=25, Elective=False))

        units.append(Unit(UnitCode='ICTE3002', Name='Human Computer Interface', Version=1, Semester=3, Credits=25, Elective=False))

        units.append(Unit(UnitCode='COMP3006', Name='Artificial and Machine Intelligence', Version=1, Semester=1, Credits=25, Elective=False))

        units.append(Unit(UnitCode='ISAD3000', Name='Capstone Computing Project 1', Version=2, Semester=3, Credits=25, Elective=False))

        units.append(Unit(UnitCode='ISAD3002', Name='Software Metrics', Version=1, Semester=1, Credits=25, Elective=False))

        units.append(Unit(UnitCode='ISEC3003', Name='Cyber Security Concepts', Version=1, Semester=1, Credits=25, Elective=False))

        units.append(Unit(UnitCode='COMP3008', Name='Distributed Computing', Version=1, Semester=1, Credits=25, Elective=False))

        units.append(Unit(UnitCode='COMP3002', Name='Theoretical Foundations of Computer Science', Version=1, Semester=2, Credits=25, Elective=False))

        units.append(Unit(UnitCode='COMP3007', Name='Machine Perception', Version=1, Semester=2, Credits=25, Elective=False))

        units.append(Unit(UnitCode='ISAD3001', Name='Capstone Computing Project 2', Version=2, Semester=3, Credits=25, Elective=False))

        units.append(Unit(UnitCode='COMP3003', Name='Software Engineering Concepts', Version=1, Semester=2, Credits=25, Elective=False))

        units.append(Unit(UnitCode='CMPE3008', Name='Software Engineering Testing', Version=1, Semester=2, Credits=25, Elective=False))

        units.append(Unit(UnitCode='ISEC3005', Name='Cyber Security- Intrusion Detection System and Incident Handling', Version=1, Semester=2, Credits=25, Elective=False))

        units.append(Unit(UnitCode='ISEC3004', Name='Cyber Crime and Security Enhanced Programming', Version=1, Semester=2, Credits=25, Elective=False))

        units.append(Unit(UnitCode='CNCO3001', Name='Network Systems Design', Version=1, Semester=2, Credits=25, Elective=False))

        units.append(Unit(UnitCode='CNCO3002', Name='Advanced Computer Communications', Version=1, Semester=1, Credits=25, Elective=False))

        units.append(Unit(UnitCode='1920', Name='Object Oriented Program Design 110', Version=8, Semester=1, Credits=25, Elective=False))

        units.append(Unit(UnitCode='8933', Name='Software Engineering 110', Version=11, Semester=1, Credits=25, Elective=False))

        units.append(Unit(UnitCode='CMHL1000', Name='Foundations For Professional Health Practice', Version=1, Semester=1, Credits=25, Elective=True))

        units.append(Unit(UnitCode='313394', Name='Foundations for Professional Health Practice 100', Version=3, Semester=1, Credits=25, Elective=True))

        units.append(Unit(UnitCode='313394', Name='Foundations for Professional Health Practice 100', Version=2, Semester=1, Credits=25, Elective=True))

        units.append(Unit(UnitCode='INDE1001', Name='Engineering Foundations - Design and Processes', Version=1, Semester=1, Credits=25, Elective=True))

        units.append(Unit(UnitCode='GEOL1002', Name='Geoscience Communication', Version=1, Semester=1, Credits=25, Elective=True))

        units.append(Unit(UnitCode='314231', Name='Engineering Foundations: Design and Processes 100', Version=1, Semester=1, Credits=25, Elective=True))

        units.append(Unit(UnitCode='312241', Name='Geoscience Communication 101', Version=2, Semester=1, Credits=25, Elective=True))

        units.append(Unit(UnitCode='307590', Name='Statistical Data Analysis 101', Version=2, Semester=2, Credits=12.5, Elective=False))

        units.append(Unit(UnitCode='1922', Name='Data Structures and Algorithms 120', Version=8, Semester=1, Credits=25, Elective=False))

        units.append(Unit(UnitCode='10163', Name='Unix and C Programming 120', Version=10, Semester=1, Credits=25, Elective=False))

        units.append(Unit(UnitCode='CMPE2004', Name='Advanced Engineering Programming', Version=1, Semester=1, Credits=25, Elective=False))

        units.append(Unit(UnitCode='310207', Name='Engineering Programming 100', Version=4, Semester=1, Credits=25, Elective=False))

        units.append(Unit(UnitCode='COMP1004', Name='Engineering Programming', Version=1, Semester=1, Credits=12.5, Elective=False))

        units.append(Unit(UnitCode='4533', Name='Database Systems 120', Version=1, Semester=1, Credits=25, Elective=False))

        units.append(Unit(UnitCode='COMP1005', Name='Fundamentals Of Programming', Version=10, Semester=1, Credits=25, Elective=False))

        units.append(Unit(UnitCode='12332', Name='Foundations of Computer Science 200', Version=3, Semester=1, Credits=25, Elective=False))

        units.append(Unit(UnitCode='MATH1004', Name='Mathematics 1', Version=1, Semester=1, Credits=25, Elective=False))

        units.append(Unit(UnitCode='4521', Name='Computer Communications 200', Version=7, Semester=1, Credits=25, Elective=False))

        units.append(Unit(UnitCode='313670', Name='Engineering Programming 210', Version=1, Semester=1, Credits=25, Elective=False))

        units.append(Unit(UnitCode='4542', Name='Operating Systems 200', Version=9, Semester=1, Credits=25, Elective=False))

        units.append(Unit(UnitCode='8934', Name='Software Engineering 200', Version=9, Semester=1, Credits=25, Elective=False))

        units.append(Unit(UnitCode='MATH1005', Name='Pre Calculus', Version=1, Semester=1, Credits=12.5, Elective=False))

        units.append(Unit(UnitCode='12333', Name='Design and Analysis of Algorithms 300', Version=6, Semester=1, Credits=25, Elective=False))

        units.append(Unit(UnitCode='314246', Name='Fundamental Concepts of Cyber Security 220', Version=1, Semester=1, Credits=25, Elective=False))

        units.append(Unit(UnitCode='314244', Name='Fundamental Concepts of Cryptography 220', Version=1, Semester=1, Credits=25, Elective=False))

        units.append(Unit(UnitCode='10926', Name='Mathematics 103', Version=5, Semester=1, Credits=25, Elective=False))

        units.append(Unit(UnitCode='307536', Name='Engineering Mathematics 120', Version=4, Semester=1, Credits=25, Elective=False))

        units.append(Unit(UnitCode='MATH1002', Name='Engineering Mathematics 1', Version=1, Semester=1, Credits=25, Elective=False))

        units.append(Unit(UnitCode='2519', Name='Unix Systems Programming 200', Version=17, Semester=1, Credits=25, Elective=False))

        units.append(Unit(UnitCode='4524', Name='Computer Graphics 200', Version=6, Semester=1, Credits=25, Elective=False))

        units.append(Unit(UnitCode='3437', Name='Programming Languages', Version=13, Semester=1, Credits=25, Elective=False))

        units.append(Unit(UnitCode='13390', Name='Requirements Engineering 252', Version=4, Semester=1, Credits=25, Elective=False))

        units.append(Unit(UnitCode='314247', Name='Network Security and Firewalls 310', Version=1, Semester=1, Credits=25, Elective=False))

        units.append(Unit(UnitCode='4529', Name='Computing Topics 251', Version=4, Semester=1, Credits=25, Elective=False))

        units.append(Unit(UnitCode='ICTE4000', Name='Human Computer Interface', Version=1, Semester=1, Credits=25, Elective=False))

        units.append(Unit(UnitCode='4517', Name='Artificial and Machine Intelligence 300', Version=8, Semester=1, Credits=25, Elective=False))

        units.append(Unit(UnitCode='7062', Name='Mathematics 101', Version=6, Semester=1, Credits=25, Elective=False))

        units.append(Unit(UnitCode='307535', Name='Engineering Mathematics 110', Version=3, Semester=1, Credits=25, Elective=False))

        units.append(Unit(UnitCode='MATH1010', Name='Advanced Mathematics', Version=1, Semester=1, Credits=25, Elective=False))

        units.append(Unit(UnitCode='MATH1000', Name='Engineering Mathematics Specialist 1', Version=1, Semester=1, Credits=25, Elective=False))

        units.append(Unit(UnitCode='ISAD4002', Name='Software Metrics', Version=1, Semester=1, Credits=25, Elective=False))

        units.append(Unit(UnitCode='314248', Name='Cyber Security Concepts 310', Version=1, Semester=1, Credits=25, Elective=False))

        units.append(Unit(UnitCode='COMP4002', Name='Extended Distributed Computing', Version=2, Semester=1, Credits=25, Elective=False))

        units.append(Unit(UnitCode='12334', Name='Theoretical Foundations of Computer Science 300', Version=5, Semester=1, Credits=25, Elective=False))

        units.append(Unit(UnitCode='COMP4001', Name='Machine Perception', Version=1, Semester=1, Credits=25, Elective=False))

        units.append(Unit(UnitCode='310288', Name='Software Engineering Project 330', Version=2, Semester=1, Credits=25, Elective=False))

        units.append(Unit(UnitCode='12335', Name='Software Engineering 300', Version=6, Semester=1, Credits=25, Elective=False))

        units.append(Unit(UnitCode='CMPE4001', Name='Extended Software Engineering Testing', Version=2, Semester=1, Credits=25, Elective=False))

        units.append(Unit(UnitCode='314250', Name='Cyber Security: Intrusion Detection System and Incident Handling 320', Version=1, Semester=1, Credits=25, Elective=False))

        units.append(Unit(UnitCode='314249', Name='Cyber Crime and Security Enhanced Programming 320', Version=1, Semester=1, Credits=25, Elective=False))

        units.append(Unit(UnitCode='ISEC4001', Name='Extended Cyber Crime and Security Enhanced Programming', Version=1, Semester=1, Credits=25, Elective=False))

        units.append(Unit(UnitCode='ISEC5007', Name='Advanced Cyber Crime and Security Enhanced Programming', Version=1, Semester=1, Credits=25, Elective=False))

        units.append(Unit(UnitCode='305684', Name='Network Systems Design 300', Version=3, Semester=1, Credits=25, Elective=False))

        units.append(Unit(UnitCode='300538', Name='Data Communications and Network Management 203', Version=2, Semester=1, Credits=25, Elective=False))

        units.append(Unit(UnitCode='CMPE2000', Name='Data Communications and Network Management', Version=1, Semester=1, Credits=25, Elective=False))

        units.append(Unit(UnitCode='4522', Name='Advanced Computer Communications 300', Version=7, Semester=1, Credits=25, Elective=False))

        units.append(Unit(UnitCode='PRJM3000', Name='Project Design and Management', Version=1, Semester=1, Credits=25, Elective=False))

        units.append(Unit(UnitCode='4549', Name='Project Design and Management 300', Version=9, Semester=1, Credits=25, Elective=False))

        units.append(Unit(UnitCode='MATH1014', Name='Foundations of Calculus', Version=1, Semester=3, Credits=25, Elective=False))

        units.append(Unit(UnitCode='ISAD3000', Name='Software Engineering Project 1', Version=1, Semester=3, Credits=25, Elective=False))

        units.append(Unit(UnitCode='310287', Name='Software Engineering Project 320', Version=2, Semester=3, Credits=25, Elective=False))

        units.append(Unit(UnitCode='ISAD3001', Name='Software Engineering Project 2', Version=1, Semester=3, Credits=25, Elective=False))

        units.append(Unit(UnitCode='ISEC3001', Name='Advanced Cryptography', Version=1, Semester=2, Credits=25, Elective=False))

        units.append(Unit(UnitCode='314245', Name='Advanced Cryptography 310', Version=1, Semester=1, Credits=25, Elective=False))

        units.append(Unit(UnitCode='314256', Name='Fundamental Concepts of Cryptography 520', Version=1, Semester=1, Credits=25, Elective=False))

        units.append(Unit(UnitCode='ISEC5002', Name='Introduction to Cryptography', Version=1, Semester=1, Credits=25, Elective=False))

        units.append(Unit(UnitCode='CMPE1000', Name='Hardware Fundamentals', Version=1, Semester=1, Credits=25, Elective=False))

        units.append(Unit(UnitCode='12702', Name='Hardware Fundamentals 101', Version=3, Semester=1, Credits=25, Elective=False))

        units.append(Unit(UnitCode='COMP4002', Name='Software Components', Version=1, Semester=1, Credits=25, Elective=False))

        units.append(Unit(UnitCode='4547', Name='Software Components 400', Version=5, Semester=1, Credits=25, Elective=False))

        units.append(Unit(UnitCode='BLAW2000', Name='Law for Engineers', Version=2, Semester=3, Credits=25, Elective=False))

        units.append(Unit(UnitCode='307664', Name='Law for Engineers 202', Version=2, Semester=1, Credits=12.5, Elective=False))

        units.append(Unit(UnitCode='ENEN2000', Name='Engineering Sustainable Development', Version=2, Semester=3, Credits=12.5, Elective=False))

        units.append(Unit(UnitCode='307660', Name='Engineering Sustainable Development 201', Version=4, Semester=3, Credits=12.5, Elective=False))

        units.append(Unit(UnitCode='PRJM2000', Name='Personal Software Processes', Version=1, Semester=1, Credits=12.5, Elective=False))

        units.append(Unit(UnitCode='308714', Name='Personal Software Processes 251', Version=1, Semester=1, Credits=25, Elective=False))

        units.append(Unit(UnitCode='ISAD4000', Name='Software Engineering Project A', Version=1, Semester=3, Credits=50, Elective=False))

        units.append(Unit(UnitCode='13396', Name='Software Engineering Project 401', Version=5, Semester=3, Credits=50, Elective=False))

        units.append(Unit(UnitCode='ISAD4001', Name='Software Engineering Project B', Version=1, Semester=3, Credits=50, Elective=False))

        units.append(Unit(UnitCode='13397', Name='Software Engineering Project 402', Version=6, Semester=3, Credits=50, Elective=False))

        units.append(Unit(UnitCode='MGMT3000', Name='Engineering Management', Version=1, Semester=3, Credits=25, Elective=False))

        units.append(Unit(UnitCode='310683', Name='Engineering Management 302', Version=1, Semester=3, Credits=25, Elective=False))

        units.append(Unit(UnitCode='MATH1007', Name='Pre and Introductory Calculus', Version=1, Semester=3, Credits=25, Elective=False))

        units.append(Unit(UnitCode='305639', Name='Mathematics 135', Version=1, Semester=3, Credits=25, Elective=False))

        units.append(Unit(UnitCode='MATH1008', Name='Calculus and Linear Algebra', Version=1, Semester=3, Credits=25, Elective=False))

        units.append(Unit(UnitCode='304640', Name='Mathematics 136', Version=1, Semester=3, Credits=25, Elective=False))

        units.append(Unit(UnitCode='ELECTIVE1', Name='Elective1', Version=1, Semester=3, Credits=25, Elective=True))

        units.append(Unit(UnitCode='ELECTIVE2', Name='Elective2', Version=1, Semester=3, Credits=25, Elective=True))

        units.append(Unit(UnitCode='ELECTIVE3', Name='Elective3', Version=1, Semester=3, Credits=25, Elective=True))

        units.append(Unit(UnitCode='ELECTIVE4', Name='Elective4', Version=1, Semester=3, Credits=25, Elective=True))

        print("Units count : " + str(len(units)))



        for entry in units:
            try:
                with transaction.atomic():
                    entry.save()

            except IntegrityError:
                # Object has already been created
                pass

        prerequisites.append(Prerequisite(UnitID=units[5], Option=1))

        prerequisites.append(Prerequisite(UnitID=units[6], Option=2))

        prerequisites.append(Prerequisite(UnitID=units[8], Option=3))

        prerequisites.append(Prerequisite(UnitID=units[8], Option=4))

        prerequisites.append(Prerequisite(UnitID=units[9], Option=5))

        prerequisites.append(Prerequisite(UnitID=units[9], Option=6))

        prerequisites.append(Prerequisite(UnitID=units[10], Option=7))

        prerequisites.append(Prerequisite(UnitID=units[10], Option=8))

        prerequisites.append(Prerequisite(UnitID=units[11], Option=9))

        prerequisites.append(Prerequisite(UnitID=units[13], Option=10))

        prerequisites.append(Prerequisite(UnitID=units[14], Option=11))

        prerequisites.append(Prerequisite(UnitID=units[15], Option=12))

        prerequisites.append(Prerequisite(UnitID=units[15], Option=13))

        prerequisites.append(Prerequisite(UnitID=units[16], Option=14))

        prerequisites.append(Prerequisite(UnitID=units[16], Option=15))

        prerequisites.append(Prerequisite(UnitID=units[17], Option=16))

        prerequisites.append(Prerequisite(UnitID=units[17], Option=17))

        prerequisites.append(Prerequisite(UnitID=units[17], Option=18))

        prerequisites.append(Prerequisite(UnitID=units[18], Option=19))

        prerequisites.append(Prerequisite(UnitID=units[18], Option=20))

        prerequisites.append(Prerequisite(UnitID=units[19], Option=21))

        prerequisites.append(Prerequisite(UnitID=units[19], Option=22))

        prerequisites.append(Prerequisite(UnitID=units[20], Option=23))

        prerequisites.append(Prerequisite(UnitID=units[21], Option=24))

        prerequisites.append(Prerequisite(UnitID=units[22], Option=25))

        prerequisites.append(Prerequisite(UnitID=units[23], Option=26))

        prerequisites.append(Prerequisite(UnitID=units[23], Option=27))

        prerequisites.append(Prerequisite(UnitID=units[24], Option=28))

        prerequisites.append(Prerequisite(UnitID=units[24], Option=29))

        prerequisites.append(Prerequisite(UnitID=units[26], Option=30))

        prerequisites.append(Prerequisite(UnitID=units[26], Option=31))

        prerequisites.append(Prerequisite(UnitID=units[27], Option=32))

        prerequisites.append(Prerequisite(UnitID=units[27], Option=33))

        prerequisites.append(Prerequisite(UnitID=units[28], Option=34))

        prerequisites.append(Prerequisite(UnitID=units[28], Option=35))

        prerequisites.append(Prerequisite(UnitID=units[29], Option=36))

        prerequisites.append(Prerequisite(UnitID=units[30], Option=37))

        prerequisites.append(Prerequisite(UnitID=units[30], Option=38))

        prerequisites.append(Prerequisite(UnitID=units[31], Option=39))

        prerequisites.append(Prerequisite(UnitID=units[32], Option=40))

        prerequisites.append(Prerequisite(UnitID=units[33], Option=41))

        prerequisites.append(Prerequisite(UnitID=units[33], Option=42))

        prerequisites.append(Prerequisite(UnitID=units[34], Option=43))

        prerequisites.append(Prerequisite(UnitID=units[35], Option=44))

        prerequisites.append(Prerequisite(UnitID=units[35], Option=45))

        prerequisites.append(Prerequisite(UnitID=units[36], Option=46))

        prerequisites.append(Prerequisite(UnitID=units[37], Option=47))

        prerequisites.append(Prerequisite(UnitID=units[1], Option=48))

        prerequisites.append(Prerequisite(UnitID=units[7], Option=49))

        prerequisites.append(Prerequisite(UnitID=units[12], Option=50))

        prerequisites.append(Prerequisite(UnitID=units[15], Option=51))

        prerequisites.append(Prerequisite(UnitID=units[25], Option=52))

        prerequisites.append(Prerequisite(UnitID=units[25], Option=53))

        prerequisites.append(Prerequisite(UnitID=units[96], Option=54))

        prerequisites.append(Prerequisite(UnitID=units[96], Option=55))

        prerequisites.append(Prerequisite(UnitID=units[96], Option=56))

        prerequisites.append(Prerequisite(UnitID=units[98], Option=57))

        prerequisites.append(Prerequisite(UnitID=units[99], Option=58))

        prerequisites.append(Prerequisite(UnitID=units[101], Option=59))

        prerequisites.append(Prerequisite(UnitID=units[102], Option=60))

        prerequisites.append(Prerequisite(UnitID=units[108], Option=61))

        prerequisites.append(Prerequisite(UnitID=units[108], Option=62))

        prerequisites.append(Prerequisite(UnitID=units[114], Option=63))

        prerequisites.append(Prerequisite(UnitID=units[116], Option=64))

        prerequisites.append(Prerequisite(UnitID=units[118], Option=65))

        print("Prerequisites count : " + str(len(prerequisites)))


        for entry in prerequisites:
            try:
                with transaction.atomic():
                    entry.save()

            except IntegrityError:
                # Object has already been created
                pass

        options.append(Options(UnitID=units[0], Option=prerequisites[0]))

        options.append(Options(UnitID=units[38], Option=prerequisites[0]))

        options.append(Options(UnitID=units[0], Option=prerequisites[1]))

        options.append(Options(UnitID=units[38], Option=prerequisites[1]))

        options.append(Options(UnitID=units[51], Option=prerequisites[1]))

        options.append(Options(UnitID=units[52], Option=prerequisites[1]))

        options.append(Options(UnitID=units[0], Option=prerequisites[2]))

        options.append(Options(UnitID=units[38], Option=prerequisites[2]))

        options.append(Options(UnitID=units[4], Option=prerequisites[3]))

        options.append(Options(UnitID=units[56], Option=prerequisites[3]))

        options.append(Options(UnitID=units[5], Option=prerequisites[4]))

        options.append(Options(UnitID=units[48], Option=prerequisites[4]))

        options.append(Options(UnitID=units[6], Option=prerequisites[5]))

        options.append(Options(UnitID=units[49], Option=prerequisites[5]))

        options.append(Options(UnitID=units[50], Option=prerequisites[5]))

        options.append(Options(UnitID=units[58], Option=prerequisites[5]))

        options.append(Options(UnitID=units[5], Option=prerequisites[6]))

        options.append(Options(UnitID=units[48], Option=prerequisites[6]))

        options.append(Options(UnitID=units[6], Option=prerequisites[7]))

        options.append(Options(UnitID=units[49], Option=prerequisites[7]))

        options.append(Options(UnitID=units[50], Option=prerequisites[7]))

        options.append(Options(UnitID=units[58], Option=prerequisites[7]))

        options.append(Options(UnitID=units[5], Option=prerequisites[8]))

        options.append(Options(UnitID=units[48], Option=prerequisites[8]))

        options.append(Options(UnitID=units[5], Option=prerequisites[9]))

        options.append(Options(UnitID=units[48], Option=prerequisites[9]))

        options.append(Options(UnitID=units[0], Option=prerequisites[10]))

        options.append(Options(UnitID=units[38], Option=prerequisites[10]))

        options.append(Options(UnitID=units[4], Option=prerequisites[11]))

        options.append(Options(UnitID=units[65], Option=prerequisites[11]))

        options.append(Options(UnitID=units[56], Option=prerequisites[11]))

        options.append(Options(UnitID=units[67], Option=prerequisites[11]))

        options.append(Options(UnitID=units[66], Option=prerequisites[11]))

        options.append(Options(UnitID=units[5], Option=prerequisites[12]))

        options.append(Options(UnitID=units[48], Option=prerequisites[12]))

        options.append(Options(UnitID=units[5], Option=prerequisites[13]))

        options.append(Options(UnitID=units[48], Option=prerequisites[13]))

        options.append(Options(UnitID=units[6], Option=prerequisites[14]))

        options.append(Options(UnitID=units[49], Option=prerequisites[14]))

        options.append(Options(UnitID=units[4], Option=prerequisites[15]))

        options.append(Options(UnitID=units[5], Option=prerequisites[16]))

        options.append(Options(UnitID=units[48], Option=prerequisites[16]))

        options.append(Options(UnitID=units[6], Option=prerequisites[17]))

        options.append(Options(UnitID=units[49], Option=prerequisites[17]))

        options.append(Options(UnitID=units[50], Option=prerequisites[17]))

        options.append(Options(UnitID=units[58], Option=prerequisites[17]))

        options.append(Options(UnitID=units[1], Option=prerequisites[18]))

        options.append(Options(UnitID=units[39], Option=prerequisites[18]))

        options.append(Options(UnitID=units[5], Option=prerequisites[19]))

        options.append(Options(UnitID=units[48], Option=prerequisites[19]))

        options.append(Options(UnitID=units[5], Option=prerequisites[20]))

        options.append(Options(UnitID=units[48], Option=prerequisites[20]))

        options.append(Options(UnitID=units[6], Option=prerequisites[21]))

        options.append(Options(UnitID=units[49], Option=prerequisites[21]))

        options.append(Options(UnitID=units[1], Option=prerequisites[22]))

        options.append(Options(UnitID=units[39], Option=prerequisites[22]))

        options.append(Options(UnitID=units[9], Option=prerequisites[23]))

        options.append(Options(UnitID=units[57], Option=prerequisites[23]))

        options.append(Options(UnitID=units[10], Option=prerequisites[24]))

        options.append(Options(UnitID=units[59], Option=prerequisites[24]))

        options.append(Options(UnitID=units[1], Option=prerequisites[25]))

        options.append(Options(UnitID=units[39], Option=prerequisites[25]))

        options.append(Options(UnitID=units[5], Option=prerequisites[26]))

        options.append(Options(UnitID=units[48], Option=prerequisites[26]))

        options.append(Options(UnitID=units[4], Option=prerequisites[27]))

        options.append(Options(UnitID=units[65], Option=prerequisites[27]))

        options.append(Options(UnitID=units[76], Option=prerequisites[27]))

        options.append(Options(UnitID=units[66], Option=prerequisites[27]))

        options.append(Options(UnitID=units[77], Option=prerequisites[27]))

        options.append(Options(UnitID=units[56], Option=prerequisites[27]))

        options.append(Options(UnitID=units[78], Option=prerequisites[27]))

        options.append(Options(UnitID=units[79], Option=prerequisites[27]))

        options.append(Options(UnitID=units[67], Option=prerequisites[27]))

        options.append(Options(UnitID=units[6], Option=prerequisites[28]))

        options.append(Options(UnitID=units[49], Option=prerequisites[28]))

        options.append(Options(UnitID=units[58], Option=prerequisites[28]))

        options.append(Options(UnitID=units[50], Option=prerequisites[28]))

        options.append(Options(UnitID=units[1], Option=prerequisites[29]))

        options.append(Options(UnitID=units[39], Option=prerequisites[29]))

        options.append(Options(UnitID=units[11], Option=prerequisites[30]))

        options.append(Options(UnitID=units[60], Option=prerequisites[30]))

        options.append(Options(UnitID=units[5], Option=prerequisites[31]))

        options.append(Options(UnitID=units[48], Option=prerequisites[31]))

        options.append(Options(UnitID=units[6], Option=prerequisites[32]))

        options.append(Options(UnitID=units[49], Option=prerequisites[32]))

        options.append(Options(UnitID=units[7], Option=prerequisites[33]))

        options.append(Options(UnitID=units[53], Option=prerequisites[33]))

        options.append(Options(UnitID=units[10], Option=prerequisites[34]))

        options.append(Options(UnitID=units[59], Option=prerequisites[34]))

        options.append(Options(UnitID=units[13], Option=prerequisites[35]))

        options.append(Options(UnitID=units[62], Option=prerequisites[35]))

        options.append(Options(UnitID=units[5], Option=prerequisites[36]))

        options.append(Options(UnitID=units[48], Option=prerequisites[36]))

        options.append(Options(UnitID=units[6], Option=prerequisites[37]))

        options.append(Options(UnitID=units[49], Option=prerequisites[37]))

        options.append(Options(UnitID=units[25], Option=prerequisites[38]))

        options.append(Options(UnitID=units[11], Option=prerequisites[39]))

        options.append(Options(UnitID=units[60], Option=prerequisites[39]))

        options.append(Options(UnitID=units[0], Option=prerequisites[40]))

        options.append(Options(UnitID=units[38], Option=prerequisites[40]))

        options.append(Options(UnitID=units[1], Option=prerequisites[41]))

        options.append(Options(UnitID=units[39], Option=prerequisites[41]))

        options.append(Options(UnitID=units[9], Option=prerequisites[42]))

        options.append(Options(UnitID=units[57], Option=prerequisites[42]))

        options.append(Options(UnitID=units[7], Option=prerequisites[43]))

        options.append(Options(UnitID=units[53], Option=prerequisites[43]))

        options.append(Options(UnitID=units[10], Option=prerequisites[44]))

        options.append(Options(UnitID=units[59], Option=prerequisites[44]))

        options.append(Options(UnitID=units[9], Option=prerequisites[45]))

        options.append(Options(UnitID=units[57], Option=prerequisites[45]))

        options.append(Options(UnitID=units[93], Option=prerequisites[45]))

        options.append(Options(UnitID=units[94], Option=prerequisites[45]))

        options.append(Options(UnitID=units[9], Option=prerequisites[46]))

        options.append(Options(UnitID=units[57], Option=prerequisites[46]))

        options.append(Options(UnitID=units[93], Option=prerequisites[46]))

        options.append(Options(UnitID=units[94], Option=prerequisites[46]))

        options.append(Options(UnitID=units[0], Option=prerequisites[47]))

        options.append(Options(UnitID=units[0], Option=prerequisites[48]))

        options.append(Options(UnitID=units[38], Option=prerequisites[48]))

        options.append(Options(UnitID=units[54], Option=prerequisites[48]))

        options.append(Options(UnitID=units[98], Option=prerequisites[49]))

        options.append(Options(UnitID=units[47], Option=prerequisites[50]))

        options.append(Options(UnitID=units[3], Option=prerequisites[50]))

        options.append(Options(UnitID=units[7], Option=prerequisites[51]))

        options.append(Options(UnitID=units[53], Option=prerequisites[51]))

        options.append(Options(UnitID=units[1], Option=prerequisites[52]))

        options.append(Options(UnitID=units[39], Option=prerequisites[52]))

        options.append(Options(UnitID=units[1], Option=prerequisites[53]))

        options.append(Options(UnitID=units[39], Option=prerequisites[53]))

        options.append(Options(UnitID=units[7], Option=prerequisites[54]))

        options.append(Options(UnitID=units[53], Option=prerequisites[54]))

        options.append(Options(UnitID=units[6], Option=prerequisites[55]))

        options.append(Options(UnitID=units[49], Option=prerequisites[55]))

        options.append(Options(UnitID=units[61], Option=prerequisites[56]))

        options.append(Options(UnitID=units[11], Option=prerequisites[57]))

        options.append(Options(UnitID=units[60], Option=prerequisites[57]))

        options.append(Options(UnitID=units[11], Option=prerequisites[58]))

        options.append(Options(UnitID=units[60], Option=prerequisites[58]))

        options.append(Options(UnitID=units[15], Option=prerequisites[59]))

        options.append(Options(UnitID=units[64], Option=prerequisites[59]))

        options.append(Options(UnitID=units[104], Option=prerequisites[59]))

        options.append(Options(UnitID=units[105], Option=prerequisites[59]))

        options.append(Options(UnitID=units[7], Option=prerequisites[60]))

        options.append(Options(UnitID=units[53], Option=prerequisites[60]))

        options.append(Options(UnitID=units[11], Option=prerequisites[61]))

        options.append(Options(UnitID=units[60], Option=prerequisites[61]))

        options.append(Options(UnitID=units[6], Option=prerequisites[62]))

        options.append(Options(UnitID=units[49], Option=prerequisites[62]))

        options.append(Options(UnitID=units[11], Option=prerequisites[63]))

        options.append(Options(UnitID=units[60], Option=prerequisites[63]))

        options.append(Options(UnitID=units[11], Option=prerequisites[64]))

        options.append(Options(UnitID=units[60], Option=prerequisites[64]))

        print("opitions count : " + str(len(options)))

        for entry in options:
            try:
                with transaction.atomic():
                    entry.save()

            except IntegrityError:
                # Object has already been created
                pass

        equivalences.append(Equivalence(UnitID=units[0], EquivID=units[38]))

        equivalences.append(Equivalence(UnitID=units[1], EquivID=units[39]))

        equivalences.append(Equivalence(UnitID=units[2], EquivID=units[40]))

        equivalences.append(Equivalence(UnitID=units[2], EquivID=units[41]))

        equivalences.append(Equivalence(UnitID=units[2], EquivID=units[42]))

        equivalences.append(Equivalence(UnitID=units[2], EquivID=units[43]))

        equivalences.append(Equivalence(UnitID=units[2], EquivID=units[44]))

        equivalences.append(Equivalence(UnitID=units[2], EquivID=units[45]))

        equivalences.append(Equivalence(UnitID=units[2], EquivID=units[46]))

        equivalences.append(Equivalence(UnitID=units[3], EquivID=units[47]))

        equivalences.append(Equivalence(UnitID=units[5], EquivID=units[48]))

        equivalences.append(Equivalence(UnitID=units[6], EquivID=units[49]))

        equivalences.append(Equivalence(UnitID=units[6], EquivID=units[50]))

        equivalences.append(Equivalence(UnitID=units[7], EquivID=units[53]))

        equivalences.append(Equivalence(UnitID=units[8], EquivID=units[55]))

        equivalences.append(Equivalence(UnitID=units[10], EquivID=units[59]))

        equivalences.append(Equivalence(UnitID=units[11], EquivID=units[60]))

        equivalences.append(Equivalence(UnitID=units[13], EquivID=units[62]))

        equivalences.append(Equivalence(UnitID=units[14], EquivID=units[63]))

        equivalences.append(Equivalence(UnitID=units[15], EquivID=units[64]))

        equivalences.append(Equivalence(UnitID=units[16], EquivID=units[68]))

        equivalences.append(Equivalence(UnitID=units[17], EquivID=units[69]))

        equivalences.append(Equivalence(UnitID=units[19], EquivID=units[70]))

        equivalences.append(Equivalence(UnitID=units[20], EquivID=units[71]))

        equivalences.append(Equivalence(UnitID=units[21], EquivID=units[72]))

        equivalences.append(Equivalence(UnitID=units[22], EquivID=units[73]))

        equivalences.append(Equivalence(UnitID=units[23], EquivID=units[74]))

        equivalences.append(Equivalence(UnitID=units[24], EquivID=units[75]))

        equivalences.append(Equivalence(UnitID=units[26], EquivID=units[80]))

        equivalences.append(Equivalence(UnitID=units[27], EquivID=units[81]))

        equivalences.append(Equivalence(UnitID=units[28], EquivID=units[82]))

        equivalences.append(Equivalence(UnitID=units[29], EquivID=units[83]))

        equivalences.append(Equivalence(UnitID=units[30], EquivID=units[84]))

        equivalences.append(Equivalence(UnitID=units[31], EquivID=units[85]))

        equivalences.append(Equivalence(UnitID=units[32], EquivID=units[86]))

        equivalences.append(Equivalence(UnitID=units[33], EquivID=units[87]))

        equivalences.append(Equivalence(UnitID=units[34], EquivID=units[88]))

        equivalences.append(Equivalence(UnitID=units[35], EquivID=units[89]))

        equivalences.append(Equivalence(UnitID=units[35], EquivID=units[90]))

        equivalences.append(Equivalence(UnitID=units[35], EquivID=units[91]))

        equivalences.append(Equivalence(UnitID=units[36], EquivID=units[92]))

        equivalences.append(Equivalence(UnitID=units[37], EquivID=units[95]))

        equivalences.append(Equivalence(UnitID=units[96], EquivID=units[97]))

        equivalences.append(Equivalence(UnitID=units[99], EquivID=units[100]))

        equivalences.append(Equivalence(UnitID=units[101], EquivID=units[85]))

        equivalences.append(Equivalence(UnitID=units[102], EquivID=units[103]))

        equivalences.append(Equivalence(UnitID=units[106], EquivID=units[107]))

        equivalences.append(Equivalence(UnitID=units[108], EquivID=units[109]))

        equivalences.append(Equivalence(UnitID=units[110], EquivID=units[111]))

        equivalences.append(Equivalence(UnitID=units[112], EquivID=units[113]))

        equivalences.append(Equivalence(UnitID=units[114], EquivID=units[115]))

        equivalences.append(Equivalence(UnitID=units[116], EquivID=units[117]))

        equivalences.append(Equivalence(UnitID=units[118], EquivID=units[119]))

        equivalences.append(Equivalence(UnitID=units[120], EquivID=units[121]))

        equivalences.append(Equivalence(UnitID=units[122], EquivID=units[123]))

        equivalences.append(Equivalence(UnitID=units[124], EquivID=units[125]))

        print("equivalences countt : " + str(len(equivalences)))


        for entry in equivalences:
            try:
                with transaction.atomic():
                    entry.save()

            except IntegrityError:
                # Object has already been created
                pass

        courses.append(Course(CourseID='STRU-CMPSC', Name='Computer Science Stream (BSc Science)', Version=1, TotalCredits=600))

        courses.append(Course(CourseID='STRU-SWENG', Name='Software Engineering Stream (BSc Science)', Version=1, TotalCredits=600))

        courses.append(Course(CourseID='STRU-CYBSC', Name='Cyber Security Stream (BSc Science)', Version=1, TotalCredits=600))

        courses.append(Course(CourseID='STRU-INFTC', Name='Information Technology Stream (BSc Science)', Version=1, TotalCredits=600))

        courses.append(Course(CourseID='313605', Name='Software Engineering Major (BEng)', Version=1, TotalCredits=600))

        print ("courses count: " + str(len(courses)))


        for entry in courses:
            try:
                with transaction.atomic():
                    entry.save()

            except IntegrityError:
                # Object has already been created
                pass

        #Computer Science stream without mid year intake
        course_templates.append(CourseTemplate(CourseID=courses[0], Option=1, MidYearEntry=False))
        course_templates.append(CourseTemplate(CourseID=courses[0], Option=2, MidYearEntry=False))

        #Computer Science stream with mid year intake
        course_templates.append(CourseTemplate(CourseID=courses[0], Option=3, MidYearEntry=True))
        course_templates.append(CourseTemplate(CourseID=courses[0], Option=4, MidYearEntry=True))

        #Software Engineering without mid year intake
        course_templates.append(CourseTemplate(CourseID=courses[1], Option=5, MidYearEntry=False))
        course_templates.append(CourseTemplate(CourseID=courses[1], Option=6, MidYearEntry=False))

        #Software Engineering with mid year intake
        course_templates.append(CourseTemplate(CourseID=courses[1], Option=7, MidYearEntry=True))
        course_templates.append(CourseTemplate(CourseID=courses[1], Option=8, MidYearEntry=True))

        #Cyber Security without mid year intake
        course_templates.append(CourseTemplate(CourseID=courses[2], Option=9, MidYearEntry=False))
        course_templates.append(CourseTemplate(CourseID=courses[2], Option=10, MidYearEntry=False))

        #Cyber security with mid year intake
        course_templates.append(CourseTemplate(CourseID=courses[2], Option=11, MidYearEntry=True))
        course_templates.append(CourseTemplate(CourseID=courses[2], Option=12, MidYearEntry=True))

        #Information technology without mid year intake
        course_templates.append(CourseTemplate(CourseID=courses[3], Option=13, MidYearEntry=False))
        course_templates.append(CourseTemplate(CourseID=courses[3], Option=14, MidYearEntry=False))

        #Information technology with mid year intake
        course_templates.append(CourseTemplate(CourseID=courses[3], Option=15, MidYearEntry=True))
        course_templates.append(CourseTemplate(CourseID=courses[3], Option=16, MidYearEntry=True))

        #BEng Software Engineering without midyear intake
        course_templates.append(CourseTemplate(CourseID=courses[4], Option=17, MidYearEntry=False))

        print("course templates count : " + str(len(course_templates)))


        for entry in course_templates:
            try:
                with transaction.atomic():
                    entry.save()

            except IntegrityError:
                # Object has already been created
                pass

        #CS 2017
        course_template_options.append(CourseTemplateOptions(Option=course_templates[0], UnitID=units[0], Year=1, Semester=1))
        course_template_options.append(CourseTemplateOptions(Option=course_templates[0], UnitID=units[1], Year=1, Semester=1))
        course_template_options.append(CourseTemplateOptions(Option=course_templates[0], UnitID=units[2], Year=1, Semester=1))
        course_template_options.append(CourseTemplateOptions(Option=course_templates[0], UnitID=units[3], Year=1, Semester=1))
        course_template_options.append(CourseTemplateOptions(Option=course_templates[0], UnitID=units[4], Year=1, Semester=1))

        course_template_options.append(CourseTemplateOptions(Option=course_templates[0], UnitID=units[5], Year=1, Semester=2))
        course_template_options.append(CourseTemplateOptions(Option=course_templates[0], UnitID=units[6], Year=1, Semester=2))
        course_template_options.append(CourseTemplateOptions(Option=course_templates[0], UnitID=units[7], Year=1, Semester=2))
        course_template_options.append(CourseTemplateOptions(Option=course_templates[0], UnitID=units[8], Year=1, Semester=2))

        course_template_options.append(CourseTemplateOptions(Option=course_templates[0], UnitID=units[9], Year=2, Semester=1))
        course_template_options.append(CourseTemplateOptions(Option=course_templates[0], UnitID=units[10], Year=2, Semester=1))
        course_template_options.append(CourseTemplateOptions(Option=course_templates[0], UnitID=units[11], Year=2, Semester=1))
        course_template_options.append(CourseTemplateOptions(Option=course_templates[0], UnitID=units[12], Year=2, Semester=1))

        course_template_options.append(CourseTemplateOptions(Option=course_templates[0], UnitID=units[17], Year=2, Semester=2))
        course_template_options.append(CourseTemplateOptions(Option=course_templates[0], UnitID=units[18], Year=2, Semester=2))
        course_template_options.append(CourseTemplateOptions(Option=course_templates[0], UnitID=units[19], Year=2, Semester=2))
        course_template_options.append(CourseTemplateOptions(Option=course_templates[0], UnitID=units[126], Year=2, Semester=2))

        course_template_options.append(CourseTemplateOptions(Option=course_templates[0], UnitID=units[23], Year=3, Semester=1))
        course_template_options.append(CourseTemplateOptions(Option=course_templates[0], UnitID=units[13], Year=3, Semester=1))
        course_template_options.append(CourseTemplateOptions(Option=course_templates[0], UnitID=units[24], Year=3, Semester=1))
        course_template_options.append(CourseTemplateOptions(Option=course_templates[0], UnitID=units[25], Year=3, Semester=1))

        course_template_options.append(CourseTemplateOptions(Option=course_templates[0], UnitID=units[127], Year=3, Semester=2))
        course_template_options.append(CourseTemplateOptions(Option=course_templates[0], UnitID=units[29], Year=3, Semester=2))
        course_template_options.append(CourseTemplateOptions(Option=course_templates[0], UnitID=units[30], Year=3, Semester=2))
        course_template_options.append(CourseTemplateOptions(Option=course_templates[0], UnitID=units[31], Year=3, Semester=2))


        #CS 2016
        course_template_options.append(CourseTemplateOptions(Option=course_templates[1], UnitID=units[4], Year=1, Semester=1))
        course_template_options.append(CourseTemplateOptions(Option=course_templates[1], UnitID=units[0], Year=1, Semester=1))
        course_template_options.append(CourseTemplateOptions(Option=course_templates[1], UnitID=units[1], Year=1, Semester=1))
        course_template_options.append(CourseTemplateOptions(Option=course_templates[1], UnitID=units[2], Year=1, Semester=1))
        course_template_options.append(CourseTemplateOptions(Option=course_templates[1], UnitID=units[3], Year=1, Semester=1))

        course_template_options.append(CourseTemplateOptions(Option=course_templates[1], UnitID=units[5], Year=1, Semester=2))
        course_template_options.append(CourseTemplateOptions(Option=course_templates[1], UnitID=units[6], Year=1, Semester=2))
        course_template_options.append(CourseTemplateOptions(Option=course_templates[1], UnitID=units[7], Year=1, Semester=2))
        course_template_options.append(CourseTemplateOptions(Option=course_templates[1], UnitID=units[126], Year=1, Semester=2))

        course_template_options.append(CourseTemplateOptions(Option=course_templates[1], UnitID=units[9], Year=2, Semester=1))
        course_template_options.append(CourseTemplateOptions(Option=course_templates[1], UnitID=units[10], Year=2, Semester=1))
        course_template_options.append(CourseTemplateOptions(Option=course_templates[1], UnitID=units[12], Year=2, Semester=1))
        course_template_options.append(CourseTemplateOptions(Option=course_templates[1], UnitID=units[127], Year=2, Semester=1))

        course_template_options.append(CourseTemplateOptions(Option=course_templates[1], UnitID=units[11], Year=2, Semester=2))
        course_template_options.append(CourseTemplateOptions(Option=course_templates[1], UnitID=units[17], Year=2, Semester=2))
        course_template_options.append(CourseTemplateOptions(Option=course_templates[1], UnitID=units[8], Year=2, Semester=2))
        course_template_options.append(CourseTemplateOptions(Option=course_templates[1], UnitID=units[19], Year=2, Semester=2))

        course_template_options.append(CourseTemplateOptions(Option=course_templates[1], UnitID=units[128], Year=3, Semester=1))
        course_template_options.append(CourseTemplateOptions(Option=course_templates[1], UnitID=units[25], Year=3, Semester=1))
        course_template_options.append(CourseTemplateOptions(Option=course_templates[1], UnitID=units[24], Year=3, Semester=1))
        course_template_options.append(CourseTemplateOptions(Option=course_templates[1], UnitID=units[13], Year=3, Semester=1))

        course_template_options.append(CourseTemplateOptions(Option=course_templates[1], UnitID=units[23], Year=3, Semester=2))
        course_template_options.append(CourseTemplateOptions(Option=course_templates[1], UnitID=units[31], Year=3, Semester=2))
        course_template_options.append(CourseTemplateOptions(Option=course_templates[1], UnitID=units[29], Year=3, Semester=2))
        course_template_options.append(CourseTemplateOptions(Option=course_templates[1], UnitID=units[30], Year=3, Semester=2))


        #CS 2017 mid
        course_template_options.append(CourseTemplateOptions(Option=course_templates[2], UnitID=units[4], Year=1, Semester=2))
        course_template_options.append(CourseTemplateOptions(Option=course_templates[2], UnitID=units[0], Year=1, Semester=2))
        course_template_options.append(CourseTemplateOptions(Option=course_templates[2], UnitID=units[8], Year=1, Semester=2))
        course_template_options.append(CourseTemplateOptions(Option=course_templates[2], UnitID=units[7], Year=1, Semester=2))

        course_template_options.append(CourseTemplateOptions(Option=course_templates[2], UnitID=units[5], Year=2, Semester=1))
        course_template_options.append(CourseTemplateOptions(Option=course_templates[2], UnitID=units[1], Year=2, Semester=1))
        course_template_options.append(CourseTemplateOptions(Option=course_templates[2], UnitID=units[2], Year=2, Semester=1))
        course_template_options.append(CourseTemplateOptions(Option=course_templates[2], UnitID=units[3], Year=2, Semester=1))
        course_template_options.append(CourseTemplateOptions(Option=course_templates[2], UnitID=units[61], Year=2, Semester=1))

        course_template_options.append(CourseTemplateOptions(Option=course_templates[2], UnitID=units[18], Year=2, Semester=2))
        course_template_options.append(CourseTemplateOptions(Option=course_templates[2], UnitID=units[6], Year=2, Semester=2))
        course_template_options.append(CourseTemplateOptions(Option=course_templates[2], UnitID=units[19], Year=2, Semester=2))
        course_template_options.append(CourseTemplateOptions(Option=course_templates[2], UnitID=units[23], Year=2, Semester=2))

        course_template_options.append(CourseTemplateOptions(Option=course_templates[2], UnitID=units[10], Year=3, Semester=1))
        course_template_options.append(CourseTemplateOptions(Option=course_templates[2], UnitID=units[13], Year=3, Semester=1))
        course_template_options.append(CourseTemplateOptions(Option=course_templates[2], UnitID=units[11], Year=3, Semester=1))
        course_template_options.append(CourseTemplateOptions(Option=course_templates[2], UnitID=units[98], Year=3, Semester=1))

        course_template_options.append(CourseTemplateOptions(Option=course_templates[2], UnitID=units[17], Year=3, Semester=2))
        course_template_options.append(CourseTemplateOptions(Option=course_templates[2], UnitID=units[25], Year=3, Semester=2))
        course_template_options.append(CourseTemplateOptions(Option=course_templates[2], UnitID=units[29], Year=3, Semester=2))
        course_template_options.append(CourseTemplateOptions(Option=course_templates[2], UnitID=units[30], Year=3, Semester=2))

        course_template_options.append(CourseTemplateOptions(Option=course_templates[2], UnitID=units[24], Year=4, Semester=1))
        course_template_options.append(CourseTemplateOptions(Option=course_templates[2], UnitID=units[31], Year=4, Semester=1))
        course_template_options.append(CourseTemplateOptions(Option=course_templates[2], UnitID=units[9], Year=4, Semester=1))
        course_template_options.append(CourseTemplateOptions(Option=course_templates[2], UnitID=units[12], Year=4, Semester=1))


        #CS 2016 mid
        course_template_options.append(CourseTemplateOptions(Option=course_templates[3], UnitID=units[124], Year=1, Semester=2))
        course_template_options.append(CourseTemplateOptions(Option=course_templates[3], UnitID=units[0], Year=1, Semester=2))
        course_template_options.append(CourseTemplateOptions(Option=course_templates[3], UnitID=units[3], Year=1, Semester=2))
        course_template_options.append(CourseTemplateOptions(Option=course_templates[3], UnitID=units[2], Year=1, Semester=2))

        course_template_options.append(CourseTemplateOptions(Option=course_templates[3], UnitID=units[5], Year=2, Semester=1))
        course_template_options.append(CourseTemplateOptions(Option=course_templates[3], UnitID=units[56], Year=2, Semester=1))
        course_template_options.append(CourseTemplateOptions(Option=course_templates[3], UnitID=units[1], Year=2, Semester=1))
        course_template_options.append(CourseTemplateOptions(Option=course_templates[3], UnitID=units[126], Year=2, Semester=1))

        course_template_options.append(CourseTemplateOptions(Option=course_templates[3], UnitID=units[11], Year=2, Semester=2))
        course_template_options.append(CourseTemplateOptions(Option=course_templates[3], UnitID=units[6], Year=2, Semester=2))
        course_template_options.append(CourseTemplateOptions(Option=course_templates[3], UnitID=units[7], Year=2, Semester=2))
        course_template_options.append(CourseTemplateOptions(Option=course_templates[3], UnitID=units[8], Year=2, Semester=2))

        course_template_options.append(CourseTemplateOptions(Option=course_templates[3], UnitID=units[9], Year=3, Semester=1))
        course_template_options.append(CourseTemplateOptions(Option=course_templates[3], UnitID=units[24], Year=3, Semester=1))
        course_template_options.append(CourseTemplateOptions(Option=course_templates[3], UnitID=units[96], Year=3, Semester=1))
        course_template_options.append(CourseTemplateOptions(Option=course_templates[3], UnitID=units[10], Year=3, Semester=1))

        course_template_options.append(CourseTemplateOptions(Option=course_templates[3], UnitID=units[17], Year=3, Semester=2))
        course_template_options.append(CourseTemplateOptions(Option=course_templates[3], UnitID=units[30], Year=3, Semester=2))
        course_template_options.append(CourseTemplateOptions(Option=course_templates[3], UnitID=units[19], Year=3, Semester=2))
        course_template_options.append(CourseTemplateOptions(Option=course_templates[3], UnitID=units[127], Year=3, Semester=2))

        course_template_options.append(CourseTemplateOptions(Option=course_templates[3], UnitID=units[13], Year=4, Semester=1))
        course_template_options.append(CourseTemplateOptions(Option=course_templates[3], UnitID=units[99], Year=4, Semester=1))
        course_template_options.append(CourseTemplateOptions(Option=course_templates[3], UnitID=units[128], Year=4, Semester=1))

        course_template_options.append(CourseTemplateOptions(Option=course_templates[3], UnitID=units[29], Year=4, Semester=2))
        course_template_options.append(CourseTemplateOptions(Option=course_templates[3], UnitID=units[101], Year=4, Semester=2))
        course_template_options.append(CourseTemplateOptions(Option=course_templates[3], UnitID=units[23], Year=4, Semester=2))


        #SE 2017
        course_template_options.append(CourseTemplateOptions(Option=course_templates[4], UnitID=units[0], Year=1, Semester=1))
        course_template_options.append(CourseTemplateOptions(Option=course_templates[4], UnitID=units[1], Year=1, Semester=1))
        course_template_options.append(CourseTemplateOptions(Option=course_templates[4], UnitID=units[2], Year=1, Semester=1))
        course_template_options.append(CourseTemplateOptions(Option=course_templates[4], UnitID=units[3], Year=1, Semester=1))
        course_template_options.append(CourseTemplateOptions(Option=course_templates[4], UnitID=units[4], Year=1, Semester=1))

        course_template_options.append(CourseTemplateOptions(Option=course_templates[4], UnitID=units[5], Year=1, Semester=2))
        course_template_options.append(CourseTemplateOptions(Option=course_templates[4], UnitID=units[6], Year=1, Semester=2))
        course_template_options.append(CourseTemplateOptions(Option=course_templates[4], UnitID=units[7], Year=1, Semester=2))
        course_template_options.append(CourseTemplateOptions(Option=course_templates[4], UnitID=units[8], Year=1, Semester=2))

        course_template_options.append(CourseTemplateOptions(Option=course_templates[4], UnitID=units[9], Year=2, Semester=1))
        course_template_options.append(CourseTemplateOptions(Option=course_templates[4], UnitID=units[10], Year=2, Semester=1))
        course_template_options.append(CourseTemplateOptions(Option=course_templates[4], UnitID=units[11], Year=2, Semester=1))
        course_template_options.append(CourseTemplateOptions(Option=course_templates[4], UnitID=units[13], Year=2, Semester=1))

        course_template_options.append(CourseTemplateOptions(Option=course_templates[4], UnitID=units[17], Year=2, Semester=2))
        course_template_options.append(CourseTemplateOptions(Option=course_templates[4], UnitID=units[18], Year=2, Semester=2))
        course_template_options.append(CourseTemplateOptions(Option=course_templates[4], UnitID=units[20], Year=2, Semester=2))
        course_template_options.append(CourseTemplateOptions(Option=course_templates[4], UnitID=units[126], Year=2, Semester=2))

        course_template_options.append(CourseTemplateOptions(Option=course_templates[4], UnitID=units[23], Year=3, Semester=1))
        course_template_options.append(CourseTemplateOptions(Option=course_templates[4], UnitID=units[26], Year=3, Semester=1))
        course_template_options.append(CourseTemplateOptions(Option=course_templates[4], UnitID=units[25], Year=3, Semester=1))
        course_template_options.append(CourseTemplateOptions(Option=course_templates[4], UnitID=units[127], Year=3, Semester=1))

        course_template_options.append(CourseTemplateOptions(Option=course_templates[4], UnitID=units[32], Year=3, Semester=2))
        course_template_options.append(CourseTemplateOptions(Option=course_templates[4], UnitID=units[33], Year=3, Semester=2))
        course_template_options.append(CourseTemplateOptions(Option=course_templates[4], UnitID=units[31], Year=3, Semester=2))
        course_template_options.append(CourseTemplateOptions(Option=course_templates[4], UnitID=units[128], Year=3, Semester=2))


        #SE 2016
        course_template_options.append(CourseTemplateOptions(Option=course_templates[5], UnitID=units[4], Year=1, Semester=1))
        course_template_options.append(CourseTemplateOptions(Option=course_templates[5], UnitID=units[0], Year=1, Semester=1))
        course_template_options.append(CourseTemplateOptions(Option=course_templates[5], UnitID=units[1], Year=1, Semester=1))
        course_template_options.append(CourseTemplateOptions(Option=course_templates[5], UnitID=units[2], Year=1, Semester=1))
        course_template_options.append(CourseTemplateOptions(Option=course_templates[5], UnitID=units[3], Year=1, Semester=1))

        course_template_options.append(CourseTemplateOptions(Option=course_templates[5], UnitID=units[5], Year=1, Semester=2))
        course_template_options.append(CourseTemplateOptions(Option=course_templates[5], UnitID=units[6], Year=1, Semester=2))
        course_template_options.append(CourseTemplateOptions(Option=course_templates[5], UnitID=units[7], Year=1, Semester=2))
        course_template_options.append(CourseTemplateOptions(Option=course_templates[5], UnitID=units[126], Year=1, Semester=2))

        course_template_options.append(CourseTemplateOptions(Option=course_templates[5], UnitID=units[9], Year=2, Semester=1))
        course_template_options.append(CourseTemplateOptions(Option=course_templates[5], UnitID=units[10], Year=2, Semester=1))
        course_template_options.append(CourseTemplateOptions(Option=course_templates[5], UnitID=units[96], Year=2, Semester=1))
        course_template_options.append(CourseTemplateOptions(Option=course_templates[5], UnitID=units[127], Year=2, Semester=1))

        course_template_options.append(CourseTemplateOptions(Option=course_templates[5], UnitID=units[11], Year=2, Semester=2))
        course_template_options.append(CourseTemplateOptions(Option=course_templates[5], UnitID=units[17], Year=2, Semester=2))
        course_template_options.append(CourseTemplateOptions(Option=course_templates[5], UnitID=units[20], Year=2, Semester=2))
        course_template_options.append(CourseTemplateOptions(Option=course_templates[5], UnitID=units[128], Year=2, Semester=2))

        course_template_options.append(CourseTemplateOptions(Option=course_templates[5], UnitID=units[15], Year=3, Semester=1))
        course_template_options.append(CourseTemplateOptions(Option=course_templates[5], UnitID=units[25], Year=3, Semester=1))
        course_template_options.append(CourseTemplateOptions(Option=course_templates[5], UnitID=units[26], Year=3, Semester=1))
        course_template_options.append(CourseTemplateOptions(Option=course_templates[5], UnitID=units[13], Year=3, Semester=1))

        course_template_options.append(CourseTemplateOptions(Option=course_templates[5], UnitID=units[23], Year=3, Semester=2))
        course_template_options.append(CourseTemplateOptions(Option=course_templates[5], UnitID=units[31], Year=3, Semester=2))
        course_template_options.append(CourseTemplateOptions(Option=course_templates[5], UnitID=units[33], Year=3, Semester=2))
        course_template_options.append(CourseTemplateOptions(Option=course_templates[5], UnitID=units[32], Year=3, Semester=2))


        #SE 2017 mid
        course_template_options.append(CourseTemplateOptions(Option=course_templates[6], UnitID=units[4], Year=1, Semester=2))
        course_template_options.append(CourseTemplateOptions(Option=course_templates[6], UnitID=units[0], Year=1, Semester=2))
        course_template_options.append(CourseTemplateOptions(Option=course_templates[6], UnitID=units[8], Year=1, Semester=2))
        course_template_options.append(CourseTemplateOptions(Option=course_templates[6], UnitID=units[7], Year=1, Semester=2))

        course_template_options.append(CourseTemplateOptions(Option=course_templates[6], UnitID=units[5], Year=2, Semester=1))
        course_template_options.append(CourseTemplateOptions(Option=course_templates[6], UnitID=units[1], Year=2, Semester=1))
        course_template_options.append(CourseTemplateOptions(Option=course_templates[6], UnitID=units[2], Year=2, Semester=1))
        course_template_options.append(CourseTemplateOptions(Option=course_templates[6], UnitID=units[3], Year=2, Semester=1))
        course_template_options.append(CourseTemplateOptions(Option=course_templates[6], UnitID=units[126], Year=2, Semester=1))

        course_template_options.append(CourseTemplateOptions(Option=course_templates[6], UnitID=units[18], Year=2, Semester=2))
        course_template_options.append(CourseTemplateOptions(Option=course_templates[6], UnitID=units[6], Year=2, Semester=2))
        course_template_options.append(CourseTemplateOptions(Option=course_templates[6], UnitID=units[33], Year=2, Semester=2))
        course_template_options.append(CourseTemplateOptions(Option=course_templates[6], UnitID=units[20], Year=2, Semester=2))

        course_template_options.append(CourseTemplateOptions(Option=course_templates[6], UnitID=units[10], Year=3, Semester=1))
        course_template_options.append(CourseTemplateOptions(Option=course_templates[6], UnitID=units[127], Year=3, Semester=1))
        course_template_options.append(CourseTemplateOptions(Option=course_templates[6], UnitID=units[11], Year=3, Semester=1))
        course_template_options.append(CourseTemplateOptions(Option=course_templates[6], UnitID=units[9], Year=3, Semester=1))

        course_template_options.append(CourseTemplateOptions(Option=course_templates[6], UnitID=units[17], Year=3, Semester=2))
        course_template_options.append(CourseTemplateOptions(Option=course_templates[6], UnitID=units[25], Year=3, Semester=2))
        course_template_options.append(CourseTemplateOptions(Option=course_templates[6], UnitID=units[32], Year=3, Semester=2))
        course_template_options.append(CourseTemplateOptions(Option=course_templates[6], UnitID=units[23], Year=3, Semester=2))

        course_template_options.append(CourseTemplateOptions(Option=course_templates[6], UnitID=units[128], Year=4, Semester=1))
        course_template_options.append(CourseTemplateOptions(Option=course_templates[6], UnitID=units[31], Year=4, Semester=1))
        course_template_options.append(CourseTemplateOptions(Option=course_templates[6], UnitID=units[26], Year=4, Semester=1))
        course_template_options.append(CourseTemplateOptions(Option=course_templates[6], UnitID=units[13], Year=4, Semester=1))


        #SE 2016 mid
        course_template_options.append(CourseTemplateOptions(Option=course_templates[7], UnitID=units[56], Year=1, Semester=2))
        course_template_options.append(CourseTemplateOptions(Option=course_templates[7], UnitID=units[0], Year=1, Semester=2))
        course_template_options.append(CourseTemplateOptions(Option=course_templates[7], UnitID=units[126], Year=1, Semester=2))
        course_template_options.append(CourseTemplateOptions(Option=course_templates[7], UnitID=units[2], Year=1, Semester=2))
        course_template_options.append(CourseTemplateOptions(Option=course_templates[7], UnitID=units[3], Year=1, Semester=2))

        course_template_options.append(CourseTemplateOptions(Option=course_templates[7], UnitID=units[5], Year=2, Semester=1))
        course_template_options.append(CourseTemplateOptions(Option=course_templates[7], UnitID=units[127], Year=2, Semester=1))
        course_template_options.append(CourseTemplateOptions(Option=course_templates[7], UnitID=units[1], Year=2, Semester=1))
        course_template_options.append(CourseTemplateOptions(Option=course_templates[7], UnitID=units[128], Year=2, Semester=1))

        course_template_options.append(CourseTemplateOptions(Option=course_templates[7], UnitID=units[11], Year=2, Semester=2))
        course_template_options.append(CourseTemplateOptions(Option=course_templates[7], UnitID=units[6], Year=2, Semester=2))
        course_template_options.append(CourseTemplateOptions(Option=course_templates[7], UnitID=units[7], Year=2, Semester=2))
        course_template_options.append(CourseTemplateOptions(Option=course_templates[7], UnitID=units[20], Year=2, Semester=2))

        course_template_options.append(CourseTemplateOptions(Option=course_templates[7], UnitID=units[9], Year=3, Semester=1))
        course_template_options.append(CourseTemplateOptions(Option=course_templates[7], UnitID=units[99], Year=3, Semester=1))
        course_template_options.append(CourseTemplateOptions(Option=course_templates[7], UnitID=units[96], Year=3, Semester=1))
        course_template_options.append(CourseTemplateOptions(Option=course_templates[7], UnitID=units[10], Year=3, Semester=1))

        course_template_options.append(CourseTemplateOptions(Option=course_templates[7], UnitID=units[17], Year=3, Semester=2))
        course_template_options.append(CourseTemplateOptions(Option=course_templates[7], UnitID=units[33], Year=3, Semester=2))
        course_template_options.append(CourseTemplateOptions(Option=course_templates[7], UnitID=units[23], Year=3, Semester=2))
        course_template_options.append(CourseTemplateOptions(Option=course_templates[7], UnitID=units[32], Year=3, Semester=2))

        course_template_options.append(CourseTemplateOptions(Option=course_templates[7], UnitID=units[13], Year=4, Semester=1))
        course_template_options.append(CourseTemplateOptions(Option=course_templates[7], UnitID=units[101], Year=4, Semester=1))
        course_template_options.append(CourseTemplateOptions(Option=course_templates[7], UnitID=units[15], Year=4, Semester=1))
        course_template_options.append(CourseTemplateOptions(Option=course_templates[7], UnitID=units[26], Year=4, Semester=1))


        #Cyber 2017
        course_template_options.append(CourseTemplateOptions(Option=course_templates[8], UnitID=units[0], Year=1, Semester=1))
        course_template_options.append(CourseTemplateOptions(Option=course_templates[8], UnitID=units[1], Year=1, Semester=1))
        course_template_options.append(CourseTemplateOptions(Option=course_templates[8], UnitID=units[2], Year=1, Semester=1))
        course_template_options.append(CourseTemplateOptions(Option=course_templates[8], UnitID=units[3], Year=1, Semester=1))
        course_template_options.append(CourseTemplateOptions(Option=course_templates[8], UnitID=units[4], Year=1, Semester=1))

        course_template_options.append(CourseTemplateOptions(Option=course_templates[8], UnitID=units[5], Year=1, Semester=2))
        course_template_options.append(CourseTemplateOptions(Option=course_templates[8], UnitID=units[6], Year=1, Semester=2))
        course_template_options.append(CourseTemplateOptions(Option=course_templates[8], UnitID=units[7], Year=1, Semester=2))
        course_template_options.append(CourseTemplateOptions(Option=course_templates[8], UnitID=units[8], Year=1, Semester=2))

        course_template_options.append(CourseTemplateOptions(Option=course_templates[8], UnitID=units[9], Year=2, Semester=1))
        course_template_options.append(CourseTemplateOptions(Option=course_templates[8], UnitID=units[10], Year=2, Semester=1))
        course_template_options.append(CourseTemplateOptions(Option=course_templates[8], UnitID=units[14], Year=2, Semester=1))
        course_template_options.append(CourseTemplateOptions(Option=course_templates[8], UnitID=units[15], Year=2, Semester=1))

        course_template_options.append(CourseTemplateOptions(Option=course_templates[8], UnitID=units[21], Year=2, Semester=2))
        course_template_options.append(CourseTemplateOptions(Option=course_templates[8], UnitID=units[22], Year=2, Semester=2))
        course_template_options.append(CourseTemplateOptions(Option=course_templates[8], UnitID=units[126], Year=2, Semester=2))
        course_template_options.append(CourseTemplateOptions(Option=course_templates[8], UnitID=units[127], Year=2, Semester=2))

        course_template_options.append(CourseTemplateOptions(Option=course_templates[8], UnitID=units[23], Year=3, Semester=1))
        course_template_options.append(CourseTemplateOptions(Option=course_templates[8], UnitID=units[27], Year=3, Semester=1))
        course_template_options.append(CourseTemplateOptions(Option=course_templates[8], UnitID=units[13], Year=3, Semester=1))
        course_template_options.append(CourseTemplateOptions(Option=course_templates[8], UnitID=units[25], Year=3, Semester=1))

        course_template_options.append(CourseTemplateOptions(Option=course_templates[8], UnitID=units[128], Year=3, Semester=2))
        course_template_options.append(CourseTemplateOptions(Option=course_templates[8], UnitID=units[34], Year=3, Semester=2))
        course_template_options.append(CourseTemplateOptions(Option=course_templates[8], UnitID=units[35], Year=3, Semester=2))
        course_template_options.append(CourseTemplateOptions(Option=course_templates[8], UnitID=units[31], Year=3, Semester=2))


        #Cyber 2016
        course_template_options.append(CourseTemplateOptions(Option=course_templates[9], UnitID=units[4], Year=1, Semester=1))
        course_template_options.append(CourseTemplateOptions(Option=course_templates[9], UnitID=units[0], Year=1, Semester=1))
        course_template_options.append(CourseTemplateOptions(Option=course_templates[9], UnitID=units[1], Year=1, Semester=1))
        course_template_options.append(CourseTemplateOptions(Option=course_templates[9], UnitID=units[2], Year=1, Semester=1))
        course_template_options.append(CourseTemplateOptions(Option=course_templates[9], UnitID=units[3], Year=1, Semester=1))

        course_template_options.append(CourseTemplateOptions(Option=course_templates[9], UnitID=units[5], Year=1, Semester=2))
        course_template_options.append(CourseTemplateOptions(Option=course_templates[9], UnitID=units[6], Year=1, Semester=2))
        course_template_options.append(CourseTemplateOptions(Option=course_templates[9], UnitID=units[7], Year=1, Semester=2))
        course_template_options.append(CourseTemplateOptions(Option=course_templates[9], UnitID=units[126], Year=1, Semester=2))

        course_template_options.append(CourseTemplateOptions(Option=course_templates[9], UnitID=units[9], Year=2, Semester=1))
        course_template_options.append(CourseTemplateOptions(Option=course_templates[9], UnitID=units[10], Year=2, Semester=1))
        course_template_options.append(CourseTemplateOptions(Option=course_templates[9], UnitID=units[15], Year=2, Semester=1))
        course_template_options.append(CourseTemplateOptions(Option=course_templates[9], UnitID=units[14], Year=2, Semester=1))

        course_template_options.append(CourseTemplateOptions(Option=course_templates[9], UnitID=units[11], Year=2, Semester=2))
        course_template_options.append(CourseTemplateOptions(Option=course_templates[9], UnitID=units[22], Year=2, Semester=2))
        course_template_options.append(CourseTemplateOptions(Option=course_templates[9], UnitID=units[21], Year=2, Semester=2))
        course_template_options.append(CourseTemplateOptions(Option=course_templates[9], UnitID=units[127], Year=2, Semester=2))

        course_template_options.append(CourseTemplateOptions(Option=course_templates[9], UnitID=units[96], Year=3, Semester=1))
        course_template_options.append(CourseTemplateOptions(Option=course_templates[9], UnitID=units[25], Year=3, Semester=1))
        course_template_options.append(CourseTemplateOptions(Option=course_templates[9], UnitID=units[27], Year=3, Semester=1))
        course_template_options.append(CourseTemplateOptions(Option=course_templates[9], UnitID=units[13], Year=3, Semester=1))

        course_template_options.append(CourseTemplateOptions(Option=course_templates[9], UnitID=units[23], Year=3, Semester=2))
        course_template_options.append(CourseTemplateOptions(Option=course_templates[9], UnitID=units[31], Year=3, Semester=2))
        course_template_options.append(CourseTemplateOptions(Option=course_templates[9], UnitID=units[35], Year=3, Semester=2))
        course_template_options.append(CourseTemplateOptions(Option=course_templates[9], UnitID=units[34], Year=3, Semester=2))


        #Cyber 2017 mid
        course_template_options.append(CourseTemplateOptions(Option=course_templates[10], UnitID=units[4], Year=1, Semester=2))
        course_template_options.append(CourseTemplateOptions(Option=course_templates[10], UnitID=units[0], Year=1, Semester=2))
        course_template_options.append(CourseTemplateOptions(Option=course_templates[10], UnitID=units[8], Year=1, Semester=2))
        course_template_options.append(CourseTemplateOptions(Option=course_templates[10], UnitID=units[7], Year=1, Semester=2))

        course_template_options.append(CourseTemplateOptions(Option=course_templates[10], UnitID=units[5], Year=2, Semester=1))
        course_template_options.append(CourseTemplateOptions(Option=course_templates[10], UnitID=units[1], Year=2, Semester=1))
        course_template_options.append(CourseTemplateOptions(Option=course_templates[10], UnitID=units[2], Year=2, Semester=1))
        course_template_options.append(CourseTemplateOptions(Option=course_templates[10], UnitID=units[3], Year=2, Semester=1))
        course_template_options.append(CourseTemplateOptions(Option=course_templates[10], UnitID=units[126], Year=2, Semester=1))

        course_template_options.append(CourseTemplateOptions(Option=course_templates[10], UnitID=units[127], Year=2, Semester=2))
        course_template_options.append(CourseTemplateOptions(Option=course_templates[10], UnitID=units[6], Year=2, Semester=2))
        course_template_options.append(CourseTemplateOptions(Option=course_templates[10], UnitID=units[128], Year=2, Semester=2))
        course_template_options.append(CourseTemplateOptions(Option=course_templates[10], UnitID=units[23], Year=2, Semester=2))

        course_template_options.append(CourseTemplateOptions(Option=course_templates[10], UnitID=units[10], Year=3, Semester=1))
        course_template_options.append(CourseTemplateOptions(Option=course_templates[10], UnitID=units[25], Year=3, Semester=1))
        course_template_options.append(CourseTemplateOptions(Option=course_templates[10], UnitID=units[27], Year=3, Semester=1))
        course_template_options.append(CourseTemplateOptions(Option=course_templates[10], UnitID=units[9], Year=3, Semester=1))

        course_template_options.append(CourseTemplateOptions(Option=course_templates[10], UnitID=units[17], Year=3, Semester=2))
        course_template_options.append(CourseTemplateOptions(Option=course_templates[10], UnitID=units[35], Year=3, Semester=2))
        course_template_options.append(CourseTemplateOptions(Option=course_templates[10], UnitID=units[22], Year=3, Semester=2))
        course_template_options.append(CourseTemplateOptions(Option=course_templates[10], UnitID=units[34], Year=3, Semester=2))

        course_template_options.append(CourseTemplateOptions(Option=course_templates[10], UnitID=units[13], Year=4, Semester=1))
        course_template_options.append(CourseTemplateOptions(Option=course_templates[10], UnitID=units[31], Year=4, Semester=1))
        course_template_options.append(CourseTemplateOptions(Option=course_templates[10], UnitID=units[14], Year=4, Semester=1))
        course_template_options.append(CourseTemplateOptions(Option=course_templates[10], UnitID=units[15], Year=4, Semester=1))


        #Cyber 2016 mid
        course_template_options.append(CourseTemplateOptions(Option=course_templates[11], UnitID=units[56], Year=1, Semester=2))
        course_template_options.append(CourseTemplateOptions(Option=course_templates[11], UnitID=units[0], Year=1, Semester=2))
        course_template_options.append(CourseTemplateOptions(Option=course_templates[11], UnitID=units[2], Year=1, Semester=2))
        course_template_options.append(CourseTemplateOptions(Option=course_templates[11], UnitID=units[3], Year=1, Semester=2))

        course_template_options.append(CourseTemplateOptions(Option=course_templates[11], UnitID=units[5], Year=2, Semester=1))
        course_template_options.append(CourseTemplateOptions(Option=course_templates[11], UnitID=units[14], Year=2, Semester=1))
        course_template_options.append(CourseTemplateOptions(Option=course_templates[11], UnitID=units[1], Year=2, Semester=1))

        course_template_options.append(CourseTemplateOptions(Option=course_templates[11], UnitID=units[11], Year=2, Semester=2))
        course_template_options.append(CourseTemplateOptions(Option=course_templates[11], UnitID=units[6], Year=2, Semester=2))
        course_template_options.append(CourseTemplateOptions(Option=course_templates[11], UnitID=units[7], Year=2, Semester=2))

        course_template_options.append(CourseTemplateOptions(Option=course_templates[11], UnitID=units[9], Year=3, Semester=1))
        course_template_options.append(CourseTemplateOptions(Option=course_templates[11], UnitID=units[10], Year=3, Semester=1))
        course_template_options.append(CourseTemplateOptions(Option=course_templates[11], UnitID=units[96], Year=3, Semester=1))
        course_template_options.append(CourseTemplateOptions(Option=course_templates[11], UnitID=units[15], Year=3, Semester=1))

        course_template_options.append(CourseTemplateOptions(Option=course_templates[11], UnitID=units[21], Year=3, Semester=2))
        course_template_options.append(CourseTemplateOptions(Option=course_templates[11], UnitID=units[23], Year=3, Semester=2))
        course_template_options.append(CourseTemplateOptions(Option=course_templates[11], UnitID=units[102], Year=3, Semester=2))
        course_template_options.append(CourseTemplateOptions(Option=course_templates[11], UnitID=units[126], Year=3, Semester=2))

        course_template_options.append(CourseTemplateOptions(Option=course_templates[11], UnitID=units[5], Year=4, Semester=1))
        course_template_options.append(CourseTemplateOptions(Option=course_templates[11], UnitID=units[99], Year=4, Semester=1))
        course_template_options.append(CourseTemplateOptions(Option=course_templates[11], UnitID=units[27], Year=4, Semester=1))
        course_template_options.append(CourseTemplateOptions(Option=course_templates[11], UnitID=units[127], Year=4, Semester=1))

        course_template_options.append(CourseTemplateOptions(Option=course_templates[11], UnitID=units[35], Year=4, Semester=2))
        course_template_options.append(CourseTemplateOptions(Option=course_templates[11], UnitID=units[101], Year=4, Semester=2))
        course_template_options.append(CourseTemplateOptions(Option=course_templates[11], UnitID=units[34], Year=4, Semester=2))


        #IT 2017
        course_template_options.append(CourseTemplateOptions(Option=course_templates[12], UnitID=units[0], Year=1, Semester=1))
        course_template_options.append(CourseTemplateOptions(Option=course_templates[12], UnitID=units[1], Year=1, Semester=1))
        course_template_options.append(CourseTemplateOptions(Option=course_templates[12], UnitID=units[2], Year=1, Semester=1))
        course_template_options.append(CourseTemplateOptions(Option=course_templates[12], UnitID=units[3], Year=1, Semester=1))
        course_template_options.append(CourseTemplateOptions(Option=course_templates[12], UnitID=units[4], Year=1, Semester=1))

        course_template_options.append(CourseTemplateOptions(Option=course_templates[12], UnitID=units[5], Year=1, Semester=2))
        course_template_options.append(CourseTemplateOptions(Option=course_templates[12], UnitID=units[6], Year=1, Semester=2))
        course_template_options.append(CourseTemplateOptions(Option=course_templates[12], UnitID=units[7], Year=1, Semester=2))
        course_template_options.append(CourseTemplateOptions(Option=course_templates[12], UnitID=units[8], Year=1, Semester=2))

        course_template_options.append(CourseTemplateOptions(Option=course_templates[12], UnitID=units[9], Year=2, Semester=1))
        course_template_options.append(CourseTemplateOptions(Option=course_templates[12], UnitID=units[10], Year=2, Semester=1))
        course_template_options.append(CourseTemplateOptions(Option=course_templates[12], UnitID=units[11], Year=2, Semester=1))
        course_template_options.append(CourseTemplateOptions(Option=course_templates[12], UnitID=units[16], Year=2, Semester=1))

        course_template_options.append(CourseTemplateOptions(Option=course_templates[12], UnitID=units[17], Year=2, Semester=2))
        course_template_options.append(CourseTemplateOptions(Option=course_templates[12], UnitID=units[22], Year=2, Semester=2))
        course_template_options.append(CourseTemplateOptions(Option=course_templates[12], UnitID=units[126], Year=2, Semester=2))
        course_template_options.append(CourseTemplateOptions(Option=course_templates[12], UnitID=units[127], Year=2, Semester=2))

        course_template_options.append(CourseTemplateOptions(Option=course_templates[12], UnitID=units[23], Year=3, Semester=1))
        course_template_options.append(CourseTemplateOptions(Option=course_templates[12], UnitID=units[14], Year=3, Semester=1))
        course_template_options.append(CourseTemplateOptions(Option=course_templates[12], UnitID=units[28], Year=3, Semester=1))
        course_template_options.append(CourseTemplateOptions(Option=course_templates[12], UnitID=units[25], Year=3, Semester=1))

        course_template_options.append(CourseTemplateOptions(Option=course_templates[12], UnitID=units[128], Year=3, Semester=2))
        course_template_options.append(CourseTemplateOptions(Option=course_templates[12], UnitID=units[36], Year=3, Semester=2))
        course_template_options.append(CourseTemplateOptions(Option=course_templates[12], UnitID=units[37], Year=3, Semester=2))
        course_template_options.append(CourseTemplateOptions(Option=course_templates[12], UnitID=units[31], Year=3, Semester=2))


        #IT 2016
        course_template_options.append(CourseTemplateOptions(Option=course_templates[13], UnitID=units[4], Year=1, Semester=1))
        course_template_options.append(CourseTemplateOptions(Option=course_templates[13], UnitID=units[0], Year=1, Semester=1))
        course_template_options.append(CourseTemplateOptions(Option=course_templates[13], UnitID=units[1], Year=1, Semester=1))
        course_template_options.append(CourseTemplateOptions(Option=course_templates[13], UnitID=units[2], Year=1, Semester=1))
        course_template_options.append(CourseTemplateOptions(Option=course_templates[13], UnitID=units[3], Year=1, Semester=1))

        course_template_options.append(CourseTemplateOptions(Option=course_templates[13], UnitID=units[5], Year=1, Semester=2))
        course_template_options.append(CourseTemplateOptions(Option=course_templates[13], UnitID=units[6], Year=1, Semester=2))
        course_template_options.append(CourseTemplateOptions(Option=course_templates[13], UnitID=units[7], Year=1, Semester=2))
        course_template_options.append(CourseTemplateOptions(Option=course_templates[13], UnitID=units[126], Year=1, Semester=2))

        course_template_options.append(CourseTemplateOptions(Option=course_templates[13], UnitID=units[9], Year=2, Semester=1))
        course_template_options.append(CourseTemplateOptions(Option=course_templates[13], UnitID=units[106], Year=2, Semester=1))
        course_template_options.append(CourseTemplateOptions(Option=course_templates[13], UnitID=units[14], Year=2, Semester=1))
        course_template_options.append(CourseTemplateOptions(Option=course_templates[13], UnitID=units[127], Year=2, Semester=1))

        course_template_options.append(CourseTemplateOptions(Option=course_templates[13], UnitID=units[11], Year=2, Semester=2))
        course_template_options.append(CourseTemplateOptions(Option=course_templates[13], UnitID=units[17], Year=2, Semester=2))
        course_template_options.append(CourseTemplateOptions(Option=course_templates[13], UnitID=units[37], Year=2, Semester=2))
        course_template_options.append(CourseTemplateOptions(Option=course_templates[13], UnitID=units[16], Year=2, Semester=2))

        course_template_options.append(CourseTemplateOptions(Option=course_templates[13], UnitID=units[10], Year=3, Semester=1))
        course_template_options.append(CourseTemplateOptions(Option=course_templates[13], UnitID=units[25], Year=3, Semester=1))
        course_template_options.append(CourseTemplateOptions(Option=course_templates[13], UnitID=units[128], Year=3, Semester=1))
        course_template_options.append(CourseTemplateOptions(Option=course_templates[13], UnitID=units[28], Year=3, Semester=1))

        course_template_options.append(CourseTemplateOptions(Option=course_templates[13], UnitID=units[23], Year=3, Semester=2))
        course_template_options.append(CourseTemplateOptions(Option=course_templates[13], UnitID=units[31], Year=3, Semester=2))
        course_template_options.append(CourseTemplateOptions(Option=course_templates[13], UnitID=units[36], Year=3, Semester=2))
        course_template_options.append(CourseTemplateOptions(Option=course_templates[13], UnitID=units[129], Year=3, Semester=2))


        #IT 2017 mid
        course_template_options.append(CourseTemplateOptions(Option=course_templates[14], UnitID=units[4], Year=1, Semester=2))
        course_template_options.append(CourseTemplateOptions(Option=course_templates[14], UnitID=units[0], Year=1, Semester=2))
        course_template_options.append(CourseTemplateOptions(Option=course_templates[14], UnitID=units[8], Year=1, Semester=2))
        course_template_options.append(CourseTemplateOptions(Option=course_templates[14], UnitID=units[7], Year=1, Semester=2))

        course_template_options.append(CourseTemplateOptions(Option=course_templates[14], UnitID=units[5], Year=2, Semester=1))
        course_template_options.append(CourseTemplateOptions(Option=course_templates[14], UnitID=units[1], Year=2, Semester=1))
        course_template_options.append(CourseTemplateOptions(Option=course_templates[14], UnitID=units[2], Year=2, Semester=1))
        course_template_options.append(CourseTemplateOptions(Option=course_templates[14], UnitID=units[3], Year=2, Semester=1))
        course_template_options.append(CourseTemplateOptions(Option=course_templates[14], UnitID=units[126], Year=2, Semester=1))

        course_template_options.append(CourseTemplateOptions(Option=course_templates[14], UnitID=units[127], Year=2, Semester=2))
        course_template_options.append(CourseTemplateOptions(Option=course_templates[14], UnitID=units[6], Year=2, Semester=2))
        course_template_options.append(CourseTemplateOptions(Option=course_templates[14], UnitID=units[128], Year=2, Semester=2))
        course_template_options.append(CourseTemplateOptions(Option=course_templates[14], UnitID=units[23], Year=2, Semester=2))

        course_template_options.append(CourseTemplateOptions(Option=course_templates[14], UnitID=units[10], Year=3, Semester=1))
        course_template_options.append(CourseTemplateOptions(Option=course_templates[14], UnitID=units[25], Year=3, Semester=1))
        course_template_options.append(CourseTemplateOptions(Option=course_templates[14], UnitID=units[11], Year=3, Semester=1))
        course_template_options.append(CourseTemplateOptions(Option=course_templates[14], UnitID=units[9], Year=3, Semester=1))

        course_template_options.append(CourseTemplateOptions(Option=course_templates[14], UnitID=units[17], Year=3, Semester=2))
        course_template_options.append(CourseTemplateOptions(Option=course_templates[14], UnitID=units[22], Year=3, Semester=2))
        course_template_options.append(CourseTemplateOptions(Option=course_templates[14], UnitID=units[37], Year=3, Semester=2))
        course_template_options.append(CourseTemplateOptions(Option=course_templates[14], UnitID=units[36], Year=3, Semester=2))

        course_template_options.append(CourseTemplateOptions(Option=course_templates[14], UnitID=units[16], Year=4, Semester=1))
        course_template_options.append(CourseTemplateOptions(Option=course_templates[14], UnitID=units[31], Year=4, Semester=1))
        course_template_options.append(CourseTemplateOptions(Option=course_templates[14], UnitID=units[14], Year=4, Semester=1))
        course_template_options.append(CourseTemplateOptions(Option=course_templates[14], UnitID=units[28], Year=4, Semester=1))


        #IT 2016 Mid
        course_template_options.append(CourseTemplateOptions(Option=course_templates[15], UnitID=units[56], Year=1, Semester=2))
        course_template_options.append(CourseTemplateOptions(Option=course_templates[15], UnitID=units[0], Year=1, Semester=2))
        course_template_options.append(CourseTemplateOptions(Option=course_templates[15], UnitID=units[126], Year=1, Semester=2))
        course_template_options.append(CourseTemplateOptions(Option=course_templates[15], UnitID=units[2], Year=1, Semester=2))
        course_template_options.append(CourseTemplateOptions(Option=course_templates[15], UnitID=units[3], Year=1, Semester=2))

        course_template_options.append(CourseTemplateOptions(Option=course_templates[15], UnitID=units[1], Year=2, Semester=1))
        course_template_options.append(CourseTemplateOptions(Option=course_templates[15], UnitID=units[5], Year=2, Semester=1))
        course_template_options.append(CourseTemplateOptions(Option=course_templates[15], UnitID=units[106], Year=2, Semester=1))
        course_template_options.append(CourseTemplateOptions(Option=course_templates[15], UnitID=units[14], Year=2, Semester=1))

        course_template_options.append(CourseTemplateOptions(Option=course_templates[15], UnitID=units[6], Year=2, Semester=2))
        course_template_options.append(CourseTemplateOptions(Option=course_templates[15], UnitID=units[7], Year=2, Semester=2))
        course_template_options.append(CourseTemplateOptions(Option=course_templates[15], UnitID=units[11], Year=2, Semester=2))
        course_template_options.append(CourseTemplateOptions(Option=course_templates[15], UnitID=units[23], Year=2, Semester=2))

        course_template_options.append(CourseTemplateOptions(Option=course_templates[15], UnitID=units[9], Year=3, Semester=1))
        course_template_options.append(CourseTemplateOptions(Option=course_templates[15], UnitID=units[10], Year=3, Semester=1))
        course_template_options.append(CourseTemplateOptions(Option=course_templates[15], UnitID=units[99], Year=3, Semester=1))
        course_template_options.append(CourseTemplateOptions(Option=course_templates[15], UnitID=units[96], Year=3, Semester=1))

        course_template_options.append(CourseTemplateOptions(Option=course_templates[15], UnitID=units[37], Year=3, Semester=2))
        course_template_options.append(CourseTemplateOptions(Option=course_templates[15], UnitID=units[16], Year=3, Semester=2))
        course_template_options.append(CourseTemplateOptions(Option=course_templates[15], UnitID=units[17], Year=3, Semester=2))
        course_template_options.append(CourseTemplateOptions(Option=course_templates[15], UnitID=units[36], Year=3, Semester=2))

        course_template_options.append(CourseTemplateOptions(Option=course_templates[15], UnitID=units[127], Year=4, Semester=1))
        course_template_options.append(CourseTemplateOptions(Option=course_templates[15], UnitID=units[128], Year=4, Semester=1))
        course_template_options.append(CourseTemplateOptions(Option=course_templates[15], UnitID=units[101], Year=4, Semester=1))
        course_template_options.append(CourseTemplateOptions(Option=course_templates[15], UnitID=units[108], Year=4, Semester=1))


        #BEng Software Engineering
        course_template_options.append(CourseTemplateOptions(Option=course_templates[16], UnitID=units[0], Year=2, Semester=1))
        course_template_options.append(CourseTemplateOptions(Option=course_templates[16], UnitID=units[1], Year=2, Semester=1))
        course_template_options.append(CourseTemplateOptions(Option=course_templates[16], UnitID=units[3], Year=2, Semester=1))
        course_template_options.append(CourseTemplateOptions(Option=course_templates[16], UnitID=units[110], Year=2, Semester=1))
        course_template_options.append(CourseTemplateOptions(Option=course_templates[16], UnitID=units[126], Year=2, Semester=1))

        course_template_options.append(CourseTemplateOptions(Option=course_templates[16], UnitID=units[5], Year=2, Semester=2))
        course_template_options.append(CourseTemplateOptions(Option=course_templates[16], UnitID=units[6], Year=2, Semester=2))
        course_template_options.append(CourseTemplateOptions(Option=course_templates[16], UnitID=units[7], Year=2, Semester=2))
        course_template_options.append(CourseTemplateOptions(Option=course_templates[16], UnitID=units[20], Year=2, Semester=2))

        course_template_options.append(CourseTemplateOptions(Option=course_templates[16], UnitID=units[9], Year=3, Semester=1))
        course_template_options.append(CourseTemplateOptions(Option=course_templates[16], UnitID=units[13], Year=3, Semester=1))
        course_template_options.append(CourseTemplateOptions(Option=course_templates[16], UnitID=units[112], Year=3, Semester=1))
        course_template_options.append(CourseTemplateOptions(Option=course_templates[16], UnitID=units[114], Year=3, Semester=1))
        course_template_options.append(CourseTemplateOptions(Option=course_templates[16], UnitID=units[127], Year=3, Semester=1))

        course_template_options.append(CourseTemplateOptions(Option=course_templates[16], UnitID=units[11], Year=3, Semester=2))
        course_template_options.append(CourseTemplateOptions(Option=course_templates[16], UnitID=units[17], Year=3, Semester=2))
        course_template_options.append(CourseTemplateOptions(Option=course_templates[16], UnitID=units[23], Year=3, Semester=2))
        course_template_options.append(CourseTemplateOptions(Option=course_templates[16], UnitID=units[33], Year=3, Semester=2))

        course_template_options.append(CourseTemplateOptions(Option=course_templates[16], UnitID=units[116], Year=4, Semester=1))
        course_template_options.append(CourseTemplateOptions(Option=course_templates[16], UnitID=units[80], Year=4, Semester=1))
        course_template_options.append(CourseTemplateOptions(Option=course_templates[16], UnitID=units[128], Year=4, Semester=1))

        course_template_options.append(CourseTemplateOptions(Option=course_templates[16], UnitID=units[118], Year=4, Semester=2))
        course_template_options.append(CourseTemplateOptions(Option=course_templates[16], UnitID=units[32], Year=4, Semester=2))
        course_template_options.append(CourseTemplateOptions(Option=course_templates[16], UnitID=units[120], Year=4, Semester=2))

        print("course_template_options count : " + str(len(course_template_options)))

        for entry in course_template_options:
            try:
                with transaction.atomic():
                    entry.save()

            except IntegrityError:
                # Object has already been created
                pass

        # ELECTIVES
        elective_templates = []
        elective_templates.append(Unit(UnitCode='ELECTIVE1', Name='ELECTIVE',  Version='1',  Credits=12.5, Semester=-1, Elective=True))
        elective_templates.append(Unit(UnitCode='ELECTIVE2', Name='ELECTIVE',  Version='1',  Credits=12.5, Semester=-1, Elective=True))
        elective_templates.append(Unit(UnitCode='ELECTIVE3', Name='ELECTIVE',  Version='1',  Credits=12.5, Semester=-1, Elective=True))
        elective_templates.append(Unit(UnitCode='ELECTIVE4', Name='ELECTIVE',  Version='1',  Credits=12.5, Semester=-1, Elective=True))

        elective_templates.append(Unit(UnitCode='ELECTIVE1', Name='ELECTIVE',  Version='2',  Credits=12.5, Semester=-1, Elective=True))
        elective_templates.append(Unit(UnitCode='ELECTIVE2', Name='ELECTIVE',  Version='2',  Credits=12.5, Semester=-1, Elective=True))
        elective_templates.append(Unit(UnitCode='ELECTIVE3', Name='ELECTIVE',  Version='2',  Credits=12.5, Semester=-1, Elective=True))
        elective_templates.append(Unit(UnitCode='ELECTIVE4', Name='ELECTIVE',  Version='2',  Credits=12.5, Semester=-1, Elective=True))

        elective_templates.append(Unit(UnitCode='ELECTIVE1', Name='ELECTIVE',  Version='1',  Credits=25.0, Semester=-1, Elective=True))
        elective_templates.append(Unit(UnitCode='ELECTIVE2', Name='ELECTIVE',  Version='1',  Credits=25.0, Semester=-1, Elective=True))
        elective_templates.append(Unit(UnitCode='ELECTIVE3', Name='ELECTIVE',  Version='1',  Credits=25.0, Semester=-1, Elective=True))
        elective_templates.append(Unit(UnitCode='ELECTIVE4', Name='ELECTIVE',  Version='1',  Credits=25.0, Semester=-1, Elective=True))

        elective_templates.append(Unit(UnitCode='ELECTIVE1', Name='ELECTIVE',  Version='2',  Credits=25.0, Semester=-1, Elective=True))
        elective_templates.append(Unit(UnitCode='ELECTIVE2', Name='ELECTIVE',  Version='2',  Credits=25.0, Semester=-1, Elective=True))
        elective_templates.append(Unit(UnitCode='ELECTIVE3', Name='ELECTIVE',  Version='2',  Credits=25.0, Semester=-1, Elective=True))
        elective_templates.append(Unit(UnitCode='ELECTIVE4', Name='ELECTIVE',  Version='2',  Credits=25.0, Semester=-1, Elective=True))

        elective_templates.append(Unit(UnitCode='ELECTIVE1', Name='ELECTIVE',  Version='1',  Credits=50.0, Semester=-1, Elective=True))
        elective_templates.append(Unit(UnitCode='ELECTIVE2', Name='ELECTIVE',  Version='1',  Credits=50.0, Semester=-1, Elective=True))
        elective_templates.append(Unit(UnitCode='ELECTIVE3', Name='ELECTIVE',  Version='1',  Credits=50.0, Semester=-1, Elective=True))
        elective_templates.append(Unit(UnitCode='ELECTIVE4', Name='ELECTIVE',  Version='1',  Credits=50.0, Semester=-1, Elective=True))

        elective_templates.append(Unit(UnitCode='ELECTIVE1', Name='ELECTIVE',  Version='2',  Credits=50.0, Semester=-1, Elective=True))
        elective_templates.append(Unit(UnitCode='ELECTIVE2', Name='ELECTIVE',  Version='2',  Credits=50.0, Semester=-1, Elective=True))
        elective_templates.append(Unit(UnitCode='ELECTIVE3', Name='ELECTIVE',  Version='2',  Credits=50.0, Semester=-1, Elective=True))
        elective_templates.append(Unit(UnitCode='ELECTIVE4', Name='ELECTIVE',  Version='2',  Credits=50.0, Semester=-1, Elective=True))

        elective_templates.append(Unit(UnitCode='ELECTIVE1', Name='ELECTIVE',  Version='1',  Credits=75.0, Semester=-1, Elective=True))
        elective_templates.append(Unit(UnitCode='ELECTIVE2', Name='ELECTIVE',  Version='1',  Credits=75.0, Semester=-1, Elective=True))
        elective_templates.append(Unit(UnitCode='ELECTIVE3', Name='ELECTIVE', Version='1',  Credits=75.0, Semester=-1, Elective=True))
        elective_templates.append(Unit(UnitCode='ELECTIVE4', Name='ELECTIVE', Version='1',  Credits=75.0, Semester=-1, Elective=True))

        elective_templates.append(Unit(UnitCode='ELECTIVE1', Name='ELECTIVE', Version='2',  Credits=75.0, Semester=-1, Elective=True))
        elective_templates.append(Unit(UnitCode='ELECTIVE2', Name='ELECTIVE', Version='2',  Credits=75.0, Semester=-1, Elective=True))
        elective_templates.append(Unit(UnitCode='ELECTIVE3', Name='ELECTIVE', Version='2',  Credits=75.0, Semester=-1, Elective=True))
        elective_templates.append(Unit(UnitCode='ELECTIVE4', Name='ELECTIVE', Version='2',  Credits=50.0, Semester=-1, Elective=True))

        ("elective_template_options count : " + str(len(elective_templates)))
        for entry in elective_templates:
            try:
                with transaction.atomic():
                    entry.save()

            except IntegrityError:
                pass

        # Function runs through all the PDF files.
        # If they are valid, processes them.
        for filename in cls.filenames:
            with open(filename, 'rb') as fp:
                file = File(fp)
                validator = PdfValidator(file)
                success, _ = validator.pdf_is_valid()
                # We still want to only use run student information saving on 'valid' PDFs.
                if success:
                    new_saver = StudentInformationSaver(validator.get_validated_information())
                    new_saver.set_student_units()
                    cls.information_savers.append(new_saver)

    def test_create_student(self):
        """
        Check that the student/s exists within the database.
        :return:
        """
        list_of_all_students = [
            '14553899',
            '16171921',
            '17898755',
            '17660585',
            # Not including the following as these students fail validation due to no course template existing.
            # '17080170',

        ]
        for student_id in list_of_all_students:
            student_exists = Student.objects.filter(StudentID=student_id).exists()
            self.assertIs(True, student_exists)

    def test_unit_electives(self):
        """
        Final Version was not implemented.
        :return:
        """
        for saver in self.information_savers:
            # saver.set_student_units()
            current_student = Student.objects.get(StudentID=saver.parsed_report['id'])
            non_computing_units = []
            all_student_elective_units = StudentUnit.objects.filter(StudentID=current_student).values(
                'UnitID__UnitCode', 'UnitID__Version')

    def test_prerequisites(self):
        """
        Final Version was not implemented.
        :return:
        """
        prerequisite_units = {
            '14553899': {
                ''
            }
        }
        for saver in self.information_savers:
            prerequisite_achieved_units = {}
            current_student = Student.objects.get(StudentID=saver.parsed_report['id'])
            list_of_units = StudentUnit.objects.all().filter(StudentID=current_student)
            for unit in list_of_units:
                if unit.PrerequisiteAchieved:
                    prerequisite_achieved_units[unit.UnitID.UnitCode] = unit.UnitID.Version

    def test_set_student_units(self):
        for saver in self.information_savers:
            saver.error_detected = False
            saver.set_student_units()
            self.assertIs(False, saver.error_detected)
