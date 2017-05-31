from django.test import TestCase
from core_app.models import Course, CourseTemplate, CourseTemplateOptions, StudentUnit, Unit
from core_app.models import Student
from core_app.views import validity_query
import json


###################################
# Unit Test for CourseProgress
###################################
class TestCourseProgress(TestCase):

    @classmethod
    def setUpTestData(cls):
        # Course
        course1 = Course.objects.create(CourseID='1688888', Name='CS', Version='2B', TotalCredits=600)

        # Student
        student1 = Student.objects.create(StudentID=16102183, Name='Chen', CreditsCompleted=500, AcademicStatus=1, CourseID=course1)

        # UNITS
        unit1 = Unit.objects.create(UnitID=123, UnitCode='abc123', Name='OOSE', Version='100', Semester=1, Credits=25.0)
        unit2 = Unit.objects.create(UnitID=456, UnitCode='abc456', Name='OOPD', Version='100', Semester=2, Credits=25.0)
        unit3 = Unit.objects.create(UnitID=789, UnitCode='abc789', Name='OS', Version='100', Semester=2, Credits=25.0)
        unit4 = Unit.objects.create(UnitID=777, UnitCode='abc777', Name='PDM', Version='300', Semester=1, Credits=25.0)
        unit5 = Unit.objects.create(UnitID=888, UnitCode='abc888', Name='CG', Version='200', Semester=1, Credits=25.0)
        unit6 = Unit.objects.create(UnitID=999, UnitCode='abc999', Name='CC', Version='200', Semester=1, Credits=25.0)
        unit7 = Unit.objects.create(UnitID=741, UnitCode='abc741', Name='Metrics', Version='200', Semester=2, Credits=25.0)
        unit8 = Unit.objects.create(UnitID=363, UnitCode='abc363', Name='HCI', Version='200', Semester=1, Credits=25.0)
        unit9 = Unit.objects.create(UnitID=369, UnitCode='abc369', Name='UCP', Version='200', Semester=2, Credits=25.0)

        # Course Temp
        courseTemp1 = CourseTemplate.objects.create(CourseID=course1, Option=163)

        # Course Temp Units
        CourseTemplateOptions.objects.create(Option=courseTemp1, UnitID=unit1, Year=1, Semester=1)
        CourseTemplateOptions.objects.create(Option=courseTemp1, UnitID=unit4, Year=1, Semester=1)
        CourseTemplateOptions.objects.create(Option=courseTemp1, UnitID=unit2, Year=1, Semester=2)
        CourseTemplateOptions.objects.create(Option=courseTemp1, UnitID=unit3, Year=1, Semester=2)
        CourseTemplateOptions.objects.create(Option=courseTemp1, UnitID=unit5, Year=2, Semester=1)
        CourseTemplateOptions.objects.create(Option=courseTemp1, UnitID=unit6, Year=2, Semester=1)
        CourseTemplateOptions.objects.create(Option=courseTemp1, UnitID=unit7, Year=2, Semester=2)
        CourseTemplateOptions.objects.create(Option=courseTemp1, UnitID=unit9, Year=2, Semester=2)

        # Student Plan Units
        StudentUnit.objects.create(StudentID=student1, UnitID=unit1, Attempts=1, Status='1', PrerequisiteAchieved=True, Year=1, Semester=1)
        StudentUnit.objects.create(StudentID=student1, UnitID=unit4, Attempts=1, Status='1', PrerequisiteAchieved=True, Year=1, Semester=1)
        StudentUnit.objects.create(StudentID=student1, UnitID=unit5, Attempts=1, Status='1', PrerequisiteAchieved=True, Year=1, Semester=1)
        StudentUnit.objects.create(StudentID=student1, UnitID=unit3, Attempts=1, Status='1', PrerequisiteAchieved=True, Year=1, Semester=2)
        StudentUnit.objects.create(StudentID=student1, UnitID=unit6, Attempts=0, Status='1', PrerequisiteAchieved=True, Year=2, Semester=1)
        StudentUnit.objects.create(StudentID=student1, UnitID=unit7, Attempts=0, Status='1', PrerequisiteAchieved=True, Year=2, Semester=2)
        StudentUnit.objects.create(StudentID=student1, UnitID=unit2, Attempts=0, Status='1', PrerequisiteAchieved=True, Year=2, Semester=2)
        StudentUnit.objects.create(StudentID=student1, UnitID=unit8, Attempts=0, Status='1', PrerequisiteAchieved=True, Year=3, Semester=1)
        StudentUnit.objects.create(StudentID=student1, UnitID=unit9, Attempts=0, Status='1', PrerequisiteAchieved=True, Year=3, Semester=2)

        raw_data= [[[{'credits': 25.0, 'id': 123}, {'credits': 25.0, 'id': 777}, {'credits': 25.0, 'id': 888}], [{'credits': 25.0, 'id': 789}]], [[{'credits': 25.0, 'id': 999}], [{'credits': 25.0, 'id': 741}, {'credits': 25.0, 'id': 456}]], [[{'credits': 25.0, 'id': 363}], [{'credits': 25.0, 'id': 369}]]]
        enrol_json_object = json.dumps(raw_data)

    def test_validity(self):
        expect_boolean = True
        student_id = 16102183
        valid_enrol_units = []
        received_plan_json = self.
        self.result_validity = validity_query()
        self.assertEqual(self.result_validity, expect_boolean)

if __name__=='__main__':
	unittest.main()
