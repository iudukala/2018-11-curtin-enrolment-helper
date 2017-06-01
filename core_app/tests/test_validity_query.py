from django.test import TestCase
from core_app.models import Course, CourseTemplate, CourseTemplateOptions, StudentUnit, Unit, Equivalence, Prerequisite, Options
from core_app.models import Student
from core_app.views import validity_query, save_student_plan
import json


###################################
# Unit Test for CourseProgress
###################################
class TestCourseProgress(TestCase):

    @classmethod
    def setUpTestData(cls):
        # Course
        course1 = Course.objects.create(CourseID='1688888', Name='Computing', Version='2B', TotalCredits=600)

        # Student
        student1 = Student.objects.create(StudentID=16102183, Name='Chen', CreditsCompleted=500, AcademicStatus=1, CourseID=course1)

        # UNITS
        unit1 = Unit.objects.create(UnitCode='123', Name='OOSE', Version='200', Semester=1, Credits=25.0)
        unit2 = Unit.objects.create(UnitCode='456', Name='OOPD', Version='200', Semester=2, Credits=25.0)
        unit3 = Unit.objects.create(UnitCode='789', Name='OS', Version='200', Semester=2, Credits=25.0)
        unit4 = Unit.objects.create(UnitCode='777', Name='PDM', Version='200', Semester=1, Credits=25.0)
        unit5 = Unit.objects.create(UnitCode='888', Name='CG', Version='200', Semester=1, Credits=25.0)
        unit6 = Unit.objects.create(UnitCode='999', Name='CC', Version='200', Semester=1, Credits=25.0)
        unit7 = Unit.objects.create(UnitCode='741', Name='Metrics', Version='200', Semester=2, Credits=25.0)
        unit8 = Unit.objects.create(UnitCode='363', Name='HCI', Version='200', Semester=1, Credits=25.0)
        unit9 = Unit.objects.create(UnitCode='369', Name='UCP', Version='200', Semester=2, Credits=25.0)

        unit10 = Unit.objects.create(UnitCode='100', Name='UP1', Version='200', Semester=1, Credits=25.0)
        unit11 = Unit.objects.create(UnitCode='101', Name='UP2', Version='200', Semester=1, Credits=25.0)
        unit12 = Unit.objects.create(UnitCode='102', Name='UP3', Version='200', Semester=1, Credits=25.0)
        unit13 = Unit.objects.create(UnitCode='103', Name='UP4', Version='200', Semester=2, Credits=25.0)
        unit14 = Unit.objects.create(UnitCode='104', Name='UP5', Version='200', Semester=2, Credits=25.0)
        unit20 = Unit.objects.create(UnitCode='3838', Name='UP38', Version='200', Semester=2, Credits=25.0)
        unit21 = Unit.objects.create(UnitCode='373', Name='UP373', Version='200', Semester=2, Credits=25.0)


        # units for equivalence
        unit15 = Unit.objects.create(UnitCode='111', Name='SE100', Version='200', Semester=1, Credits=25.0)
        unit16 = Unit.objects.create(UnitCode='222', Name='SE200', Version='200', Semester=2, Credits=25.0)
        # units for prerequisite
        unit17 = Unit.objects.create(UnitCode='333', Name='SE300', Version='200', Semester=1, Credits=25.0)
        unit18 = Unit.objects.create(UnitCode='444', Name='SEP1', Version='200', Semester=2, Credits=25.0)
        # a elective unit
        unit19 = Unit.objects.create(UnitCode='666', Name='CCP', Version='200', Semester=1, Credits=25.0, Elective=True)

        # Course Temp
        courseTemp1 = CourseTemplate.objects.create(CourseID=course1, Option=163)
        courseTemp2 = CourseTemplate.objects.create(CourseID=course1, Option=167)

        # Equivalence
        equivalence1 = Equivalence.objects.create(UnitID=unit10, EquivID=unit15)
        equivalence2 = Equivalence.objects.create(UnitID=unit11, EquivID=unit16)

        # Prerequisite
        prerequisite1 = Prerequisite.objects.create(Option=711, UnitID=unit12)
        prerequisite2 = Prerequisite.objects.create(Option=722, UnitID=unit13)

        # Options
        option1 = Options.objects.create(UnitID=unit17, Option=prerequisite1)
        option2 = Options.objects.create(UnitID=unit18, Option=prerequisite2)

        # Course Temp Options
            # for test_1
        CourseTemplateOptions.objects.create(Option=courseTemp1, UnitID=unit1, Year=1, Semester=1)
        CourseTemplateOptions.objects.create(Option=courseTemp1, UnitID=unit4, Year=1, Semester=1)
        CourseTemplateOptions.objects.create(Option=courseTemp1, UnitID=unit5, Year=1, Semester=1)
        CourseTemplateOptions.objects.create(Option=courseTemp1, UnitID=unit3, Year=1, Semester=2)
        CourseTemplateOptions.objects.create(Option=courseTemp1, UnitID=unit6, Year=2, Semester=1)
        CourseTemplateOptions.objects.create(Option=courseTemp1, UnitID=unit7, Year=2, Semester=2)
        CourseTemplateOptions.objects.create(Option=courseTemp1, UnitID=unit2, Year=2, Semester=2)
        CourseTemplateOptions.objects.create(Option=courseTemp1, UnitID=unit8, Year=3, Semester=1)
        CourseTemplateOptions.objects.create(Option=courseTemp1, UnitID=unit9, Year=3, Semester=2)


            # for test_2 test_3 test_4
        CourseTemplateOptions.objects.create(Option=courseTemp1, UnitID=unit15, Year=1, Semester=1)
        CourseTemplateOptions.objects.create(Option=courseTemp1, UnitID=unit16, Year=1, Semester=2)
        CourseTemplateOptions.objects.create(Option=courseTemp1, UnitID=unit17, Year=2, Semester=1)
        CourseTemplateOptions.objects.create(Option=courseTemp1, UnitID=unit18, Year=2, Semester=2)

        CourseTemplateOptions.objects.create(Option=courseTemp1, UnitID=unit10, Year=3, Semester=1)
        CourseTemplateOptions.objects.create(Option=courseTemp1, UnitID=unit11, Year=3, Semester=1)
        CourseTemplateOptions.objects.create(Option=courseTemp1, UnitID=unit12, Year=3, Semester=1)
        CourseTemplateOptions.objects.create(Option=courseTemp1, UnitID=unit13, Year=3, Semester=2)
        CourseTemplateOptions.objects.create(Option=courseTemp1, UnitID=unit14, Year=3, Semester=2)
        CourseTemplateOptions.objects.create(Option=courseTemp1, UnitID=unit20, Year=3, Semester=2)
        CourseTemplateOptions.objects.create(Option=courseTemp1, UnitID=unit21, Year=3, Semester=2)

          # a elective unit available in course templates
        CourseTemplateOptions.objects.create(Option=courseTemp2, UnitID=unit19, Year=3, Semester=1)


        # Student Plan Units
            # student units for equivalence
        StudentUnit.objects.create(StudentID=student1, UnitID=unit15, Attempts=1, Status=3, PrerequisiteAchieved=True, Year=1, Semester=1)
        StudentUnit.objects.create(StudentID=student1, UnitID=unit16, Attempts=0, Status=2, PrerequisiteAchieved=True, Year=1, Semester=2)
            # student units for prerequisite
        StudentUnit.objects.create(StudentID=student1, UnitID=unit17, Attempts=1, Status=3, PrerequisiteAchieved=True, Year=2, Semester=1)
        StudentUnit.objects.create(StudentID=student1, UnitID=unit18, Attempts=1, Status=2, PrerequisiteAchieved=True, Year=2, Semester=2)


    # without any previous enrolments before
    def test_validity_1(self):
        expect_boolean = True
        student_id = 16102183
        error_message = ''
        valid_enrol_units = []
        valid_enrol_dict = {}
        new_plan_1 = [[[{'credits': 25.0, 'id': 123, 'version' : 200, 'course_version' : '2B'}, {'credits': 25.0, 'id': 777, 'version' : 200, 'course_version' : '2B'}, {'credits': 25.0, 'id': 888, 'version' : 200, 'course_version' : '2B'}], [{'credits': 25.0, 'id': 789, 'version' : 200, 'course_version' : '2B'}]], [[{'credits': 25.0, 'id': 999, 'version' : 200, 'course_version' : '2B'}], [{'credits': 25.0, 'id': 741, 'version' : 200, 'course_version' : '2B'}, {'credits': 25.0, 'id': 456, 'version' : 200, 'course_version' : '2B'}]], [[{'credits': 25.0, 'id': 363, 'version' : 200, 'course_version' : '2B'}], [{'credits': 25.0, 'id': 369, 'version' : 200, 'course_version' : '2B'}]]]

        self.result_validity = validity_query(new_plan_1, valid_enrol_dict, valid_enrol_units, student_id, error_message)
        self.assertEqual(self.result_validity, expect_boolean)

    # test case: include a unit that has a equiv unit already passed in previous plan, we can not enrol that unit
    # {'credits' : 25.0, 'id' : 101} its equivalence already passed in previous plan
    def test_validity_2(self):
        expect_boolean = False
        student_id = 16102183
        error_message = ''
        valid_enrol_units = []
        valid_enrol_dict = {}
        new_plan_2 = [[[{'credits': 25.0, 'id': 123, 'version' : 200, 'course_version' : '2B'}, {'credits': 25.0, 'id': 777, 'version' : 200, 'course_version' : '2B'}, {'credits': 25.0, 'id': 888, 'version' : 200, 'course_version' : '2B'}], [{'credits': 25.0, 'id': 789, 'version' : 200, 'course_version' : '2B'}]], [[{'credits': 25.0, 'id': 999, 'version' : 200, 'course_version' : '2B'}], [{'credits': 25.0, 'id': 741, 'version' : 200, 'course_version' : '2B'}, {'credits': 25.0, 'id': 456, 'version' : 200, 'course_version' : '2B'}]], [[{'credits': 25.0, 'id': 363, 'version' : 200, 'course_version' : '2B'}, {'credits' : 25.0, 'id' : 101, 'version' : 200, 'course_version' : '2B'}], [{'credits': 25.0, 'id': 369, 'version' : 200, 'course_version' : '2B'}]]]

        self.result_validity = validity_query(new_plan_2, valid_enrol_dict, valid_enrol_units, student_id, error_message)
        self.assertEqual(self.result_validity, expect_boolean)

    # test case: include a unit that has a equiv unit but did not pass in previous plan, we can enrol that unit
    # {'credits' : 25.0, 'id' : 100} its equivalence was failed in previous plan
    def test_validity_3(self):
        expect_boolean = True
        student_id = 16102183
        error_message = ''
        valid_enrol_units = []
        valid_enrol_dict = {}
        new_plan_3 = [[[{'credits': 25.0, 'id': 123, 'version' : 200, 'course_version' : '2B'}, {'credits': 25.0, 'id': 777, 'version' : 200, 'course_version' : '2B'}, {'credits': 25.0, 'id': 888, 'version' : 200, 'course_version' : '2B'}], [{'credits': 25.0, 'id': 789, 'version' : 200, 'course_version' : '2B'}]], [[{'credits': 25.0, 'id': 999, 'version' : 200, 'course_version' : '2B'}], [{'credits': 25.0, 'id': 741, 'version' : 200, 'course_version' : '2B'}, {'credits': 25.0, 'id': 456, 'version' : 200, 'course_version' : '2B'}]], [[{'credits': 25.0, 'id': 363, 'version' : 200, 'course_version' : '2B'}, {'credits' : 25.0, 'id' : 100, 'version' : 200, 'course_version' : '2B'}], [{'credits': 25.0, 'id': 369, 'version' : 200, 'course_version' : '2B'}]]]

        self.result_validity = validity_query(new_plan_3, valid_enrol_dict, valid_enrol_units, student_id, error_message)
        self.assertEqual(self.result_validity, expect_boolean)

    # test case: include a unit that a prerequisite unit did not pass in previous plan, we can not enrol that unit
    # {'credits' : 25.0, 'id' : 102} its prerequisite was failed
    def test_validity_4(self):
        expect_boolean = False
        student_id = 16102183
        error_message = ''
        valid_enrol_units = []
        valid_enrol_dict = {}
        new_plan_4 = [[[{'credits': 25.0, 'id': 123, 'version' : 200, 'course_version' : '2B'}, {'credits': 25.0, 'id': 777, 'version' : 200, 'course_version' : '2B'}, {'credits': 25.0, 'id': 888, 'version' : 200, 'course_version' : '2B'}], [{'credits': 25.0, 'id': 789, 'version' : 200, 'course_version' : '2B'}]], [[{'credits': 25.0, 'id': 999, 'version' : 200, 'course_version' : '2B'}], [{'credits': 25.0, 'id': 741, 'version' : 200, 'course_version' : '2B'}, {'credits': 25.0, 'id': 456, 'version' : 200, 'course_version' : '2B'}]], [[{'credits': 25.0, 'id': 363, 'version' : 200, 'course_version' : '2B'}, {'credits' : 25.0, 'id' : 102, 'version' : 200, 'course_version' : '2B'}], [{'credits': 25.0, 'id': 369, 'version' : 200, 'course_version' : '2B'}]]]

        self.result_validity = validity_query(new_plan_4, valid_enrol_dict, valid_enrol_units, student_id, error_message)
        self.assertEqual(self.result_validity, expect_boolean)

    # test case: include a unit that a prerequisite unit has passed in previous plan, we can enrol that unit
    #
    def test_validity_5(self):
        expect_boolean = True
        student_id = 16102183
        error_message = ''
        valid_enrol_units = []
        valid_enrol_dict = {}
        new_plan_5 = [[[{'credits': 25.0, 'id': 123, 'version' : 200, 'course_version' : '2B'}, {'credits': 25.0, 'id': 777, 'version' : 200, 'course_version' : '2B'}, {'credits': 25.0, 'id': 888, 'version' : 200, 'course_version' : '2B'}], [{'credits': 25.0, 'id': 789, 'version' : 200, 'course_version' : '2B'}]], [[{'credits': 25.0, 'id': 999, 'version' : 200, 'course_version' : '2B'}], [{'credits': 25.0, 'id': 741, 'version' : 200, 'course_version' : '2B'}, {'credits': 25.0, 'id': 456, 'version' : 200, 'course_version' : '2B'}]], [[{'credits': 25.0, 'id': 363, 'version' : 200, 'course_version' : '2B'}], [{'credits': 25.0, 'id': 369, 'version' : 200, 'course_version' : '2B'}, {'credits' : 25.0, 'id' : 103, 'version' : 200, 'course_version' : '2B'}]]]

        self.result_validity = validity_query(new_plan_5, valid_enrol_dict, valid_enrol_units, student_id, error_message)
        self.assertEqual(self.result_validity, expect_boolean)

    # test case: a smester include more than 100 credits
    # the year 3 semester 2, unit 13 14 20 21 18 total credits is more than 100, will false
    def test_validity_6(self):
        expect_boolean = False
        student_id = 16102183
        error_message = ''
        valid_enrol_units = []
        valid_enrol_dict = {}
        new_plan_6 = [[[{'credits': 25.0, 'id': 123, 'version' : 200, 'course_version' : '2B'}, {'credits': 25.0, 'id': 777, 'version' : 200, 'course_version' : '2B'}, {'credits': 25.0, 'id': 888, 'version' : 200, 'course_version' : '2B'}], [{'credits': 25.0, 'id': 789, 'version' : 200, 'course_version' : '2B'}]], [[{'credits': 25.0, 'id': 999, 'version' : 200, 'course_version' : '2B'}], [{'credits': 25.0, 'id': 741, 'version' : 200, 'course_version' : '2B'}, {'credits': 25.0, 'id': 456, 'version' : 200, 'course_version' : '2B'}]], [[{'credits': 25.0, 'id': 363, 'version' : 200, 'course_version' : '2B'}], [{'credits': 25.0, 'id': 369, 'version' : 200, 'course_version' : '2B'}, {'credits' : 25.0, 'id' : 103, 'version' : 200, 'course_version' : '2B'}, {'credits' : 25.0, 'id' : 373, 'version' : 200, 'course_version' : '2B'}, {'credits' : 25.0, 'id' : 104, 'version' : 200, 'course_version' : '2B'}, {'credits' : 25.0, 'id' : 3838, 'version' : 200, 'course_version' : '2B'}]]]

        self.result_validity = validity_query(new_plan_6, valid_enrol_dict, valid_enrol_units, student_id, error_message)
        self.assertEqual(self.result_validity, expect_boolean)

    # a new enrollment plan includes a elective unit {'credits': 25.0, 'id': 666} and other units, checking if the can store the all valid units into a list properly
    # valid_enrol_units list will store all unit id in new_plan_7 list because they all are allowed to enrol, so will return true
    def test_validity_7(self):
        expect_list = [123, 777, 888, 789, 999, 741, 456, 363, 666, 369]
        student_id = 16102183
        error_message = ''
        valid_enrol_units = []
        valid_enrol_dict = {}
        new_plan_7 = [[[{'credits': 25.0, 'id': 123, 'version' : 200, 'course_version' : '2B'}, {'credits': 25.0, 'id': 777, 'version' : 200, 'course_version' : '2B'}, {'credits': 25.0, 'id': 888, 'version' : 200, 'course_version' : '2B'}], [{'credits': 25.0, 'id': 789, 'version' : 200, 'course_version' : '2B'}]], [[{'credits': 25.0, 'id': 999, 'version' : 200, 'course_version' : '2B'}], [{'credits': 25.0, 'id': 741, 'version' : 200, 'course_version' : '2B'}, {'credits': 25.0, 'id': 456, 'version' : 200, 'course_version' : '2B'}]], [[{'credits': 25.0, 'id': 363, 'version' : 200, 'course_version' : '2B'}, {'credits': 25.0, 'id': 666, 'version' : 200, 'course_version' : '2B'}], [{'credits': 25.0, 'id': 369, 'version' : 200, 'course_version' : '2B'}]]]

        self.result_validity = validity_query(new_plan_7, valid_enrol_dict, valid_enrol_units, student_id, error_message)
        self.assertEqual(valid_enrol_units, expect_list)

    # only 1 unit in enrolment plan and it is not allowed to enrol because prerequis was failed before
    # will return False
    def test_validity_8(self):
        expect_boolean = False
        student_id = 16102183
        error_message = ''
        valid_enrol_units = []
        valid_enrol_dict = {}
        new_plan_8 = [[[{'credits': 25.0, 'id': 102, 'version' : 200, 'course_version' : '2B'}]]]

        self.result_validity = validity_query(new_plan_8, valid_enrol_dict, valid_enrol_units, student_id, error_message)
        self.assertEqual(self.result_validity, expect_boolean)

    # this for testing save the newly created student enrolment plan to the database.
    def test_save_student_plan(self):
        expect_boolean = True
        student_id = 16102183
        valid_enrol_dict = {'123':{'version':'200', 'credits':25.0}, '456':{'version':'200', 'credits':25.0}}
        valid_enrol_units = ['123', '456']
        self.result_save = save_student_plan(valid_enrol_dict, valid_enrol_units, student_id)
        self.assertEqual(self.result_save, expect_boolean)

if __name__=='__main__':
	unittest.main()
