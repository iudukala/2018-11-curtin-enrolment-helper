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
        unit1 = Unit.objects.create(UnitCode='123', Name='OOSE', Version='200', Semester=1, Credits=25.0)
        unit2 = Unit.objects.create(UnitCode='456', Name='OOPD', Version='200', Semester=2, Credits=25.0)
        unit3 = Unit.objects.create(UnitCode='789', Name='OS', Version='200', Semester=2, Credits=25.0)
        unit4 = Unit.objects.create(UnitCode='777', Name='PDM', Version='200', Semester=1, Credits=25.0)
        unit5 = Unit.objects.create(UnitCode='888', Name='CG', Version='200', Semester=1, Credits=25.0)
        unit6 = Unit.objects.create(UnitCode='999', Name='CC', Version='200', Semester=1, Credits=25.0)
        unit7 = Unit.objects.create(UnitCode='741', Name='Metrics', Version='200', Semester=2, Credits=25.0)
        unit8 = Unit.objects.create(UnitCode='363', Name='HCI', Version='200', Semester=1, Credits=25.0)
        unit9 = Unit.objects.create(UnitCode='369', Name='UCP', Version='200', Semester=2, Credits=25.0)

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


    # this is for testing function can form course information correct
    def test_course_dict(self):
        expect_course = {'course_version': '2B', 'name': 'CS', 'id': '1688888'}
        student_id = 16102183
        student = Student.objects.get(pk=student_id)
        self.courses = form_course(student)
        self.assertEqual(self.courses, expect_course)

    # this is for testing function can form course templates units correct, pass
    def test_templates_dict(self):
        expect_temp = [[[{'status': 1, 'attempts': 1, 'name': 'OOSE', 'version': '200', 'credits': 25.0, 'id': '123'}, {'status': 1, 'attempts': 1, 'name': 'PDM', 'version': '200', 'credits': 25.0, 'id': '777'}], [{'status': 1, 'attempts': 0, 'name': 'OOPD', 'version': '200', 'credits': 25.0, 'id': '456'}, {'status': 1, 'attempts': 1, 'name': 'OS', 'version': '200', 'credits': 25.0, 'id': '789'}]], [[{'status': 1, 'attempts': 1, 'name': 'CG', 'version': '200', 'credits': 25.0, 'id': '888'}, {'status': 1, 'attempts': 0, 'name': 'CC', 'version': '200', 'credits': 25.0, 'id': '999'}], [{'status': 1, 'attempts': 0, 'name': 'Metrics', 'version': '200', 'credits': 25.0, 'id': '741'}, {'status': 1, 'attempts': 0, 'name': 'UCP', 'version': '200', 'credits': 25.0, 'id': '369'}]]]
        student_id = 16102183
        student = Student.objects.get(StudentID=16102183)
        course = student.CourseID
        all_course_temp = CourseTemplate.objects.all().filter(CourseID=course)
        self.templates = form_templates(all_course_temp, student_id)
        self.assertEqual(self.templates, expect_temp)

    # his is for testing function can form plan units correct, pass
    def test_plans_dict(self):
        expect_plan = [[[{'id': '123', 'version': '200', 'credits': 25.0}, {'id': '777', 'version': '200', 'credits': 25.0}, {'id': '888', 'version': '200', 'credits': 25.0}], [{'id': '789', 'version': '200', 'credits': 25.0}]], [[{'id': '999', 'version': '200', 'credits': 25.0}], [{'id': '741', 'version': '200', 'credits': 25.0}, {'id': '456', 'version': '200', 'credits': 25.0}]], [[{'id': '363', 'version': '200', 'credits': 25.0}], [{'id': '369', 'version': '200', 'credits': 25.0}]]]
        student = Student.objects.get(StudentID=16102183)
        all_plan = StudentUnit.objects.all().filter(StudentID=student.StudentID).order_by('Year', 'Semester')
        self.plans = form_plans(all_plan)
        self.assertEqual(self.plans, expect_plan)

    # # this test is for testing only one plan in db, pass in a plan unit(id 123) expect [[[{'credits': 25.0, 'id': 123}]]], actual output is
    # # [[[{'credits': 25.0, 'id': 123}]]], return true
    # def test_single_plan(self):
    #     expect_plan = [[[{'id': '123', 'version': '200', 'credits': 25.0}]]]
    #     student = Student.objects.get(StudentID=16102183)
    #     all_plan = StudentUnit.objects.all().filter(StudentID=student).order_by('Year', 'Semester')
    #     self.plans = form_plans(all_plan)
    #     self.assertEqual(self.plans, expect_plan)


if __name__=='__main__':
	unittest.main()
