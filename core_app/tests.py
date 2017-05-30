from django.test import TestCase
from core_app.models import Course, CourseTemplate, CourseTemplateOptions, StudentUnit, Unit
from core_app.models import Student
from core_app.views import form_templates, form_plans, form_course


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


    def test_course_dict(self):
        expect_course = {'id': '1688888', 'name': 'CS'}
        student_id = 16102183
        student = Student.objects.get(pk=student_id)
        self.courses = form_course(student)
        self.assertEqual(self.courses, expect_course)

    def test_templates_dict(self):
        expect_temp = [[[{'credits': 25.0, 'id': 123, 'name': 'OOSE', 'attempts': 1, 'status': 1}, {'credits': 25.0, 'id': 777, 'name': 'PDM', 'attempts': 1, 'status': 1}], [{'credits': 25.0, 'id': 456, 'name': 'OOPD', 'attempts': 0, 'status': 1}, {'credits': 25.0, 'id': 789, 'name': 'OS', 'attempts': 1, 'status': 1}]], [[{'credits': 25.0, 'id': 888, 'name': 'CG', 'attempts': 1, 'status': 1}, {'credits': 25.0, 'id': 999, 'name': 'CC', 'attempts': 0, 'status': 1}], [{'credits': 25.0, 'id': 741, 'name': 'Metrics', 'attempts': 0, 'status': 1}, {'credits': 25.0, 'id': 369, 'name': 'UCP', 'attempts': 0, 'status': 1}]]]
        student_id = 16102183
        student = Student.objects.get(StudentID=16102183)
        course = Course.objects.get(CourseID=student.CourseID.CourseID)
        all_course_temp = CourseTemplate.objects.all().filter(CourseID=course.CourseID)
        self.templates = form_templates(all_course_temp, student_id)
        self.assertEqual(self.templates, expect_temp)

    def test_plans_dict(self):
        expect_plan = [[[{'credits': 25.0, 'id': 123}, {'credits': 25.0, 'id': 777}, {'credits': 25.0, 'id': 888}], [{'credits': 25.0, 'id': 789}]], [[{'credits': 25.0, 'id': 999}], [{'credits': 25.0, 'id': 741}, {'credits': 25.0, 'id': 456}]], [[{'credits': 25.0, 'id': 363}], [{'credits': 25.0, 'id': 369}]]]
        student = Student.objects.get(StudentID=16102183)
        all_plan = StudentUnit.objects.all().filter(StudentID=student.StudentID).order_by('Year', 'Semester')
        self.plans = form_plans(all_plan)
        self.assertEqual(self.plans, expect_plan)


if __name__=='__main__':
	unittest.main()
