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
        unit5 = Unit.objects.create(UnitID=888, UnitCode='abc888', Name='CG', Version='200', Semester=2, Credits=25.0)

        # Course Temp
        courseTemp1 = CourseTemplate.objects.create(CourseID=course1, Option=163)

        # Course Temp Units
        CourseTemplateOptions.objects.create(Option=courseTemp1, UnitID=unit1, Year=1, Semester=1)
        CourseTemplateOptions.objects.create(Option=courseTemp1, UnitID=unit2, Year=2, Semester=2)
        CourseTemplateOptions.objects.create(Option=courseTemp1, UnitID=unit3, Year=3, Semester=2)
        CourseTemplateOptions.objects.create(Option=courseTemp1, UnitID=unit4, Year=2, Semester=1)
        CourseTemplateOptions.objects.create(Option=courseTemp1, UnitID=unit5, Year=3, Semester=2)

        # Student Plan Units
        StudentUnit.objects.create(StudentID=student1, UnitID=unit1, Attempts=1, Status='1', PrerequisiteAchieved=True, Year=1, Semester=1)
        StudentUnit.objects.create(StudentID=student1, UnitID=unit2, Attempts=0, Status='1', PrerequisiteAchieved=True, Year=2, Semester=2)
        StudentUnit.objects.create(StudentID=student1, UnitID=unit3, Attempts=0, Status='1', PrerequisiteAchieved=True, Year=3, Semester=2)


    def test_course_dict(self):
        student_id = 16102183
        student = Student.objects.get(pk=student_id)
        self.courses = form_course(student)
        print(self.courses)

    def test_templates_dict(self):
        student_id = 16102183
        student = Student.objects.get(StudentID=16102183)
        course = Course.objects.get(CourseID=student.CourseID.CourseID)
        all_course_temp = CourseTemplate.objects.all().filter(CourseID=course.CourseID)
        self.templates = form_templates(all_course_temp, student_id)
        print(self.templates)

    def test_plans_dict(self):
        student = Student.objects.get(StudentID=16102183)
        all_plan = StudentUnit.objects.all().filter(StudentID=student.StudentID).order_by('Year', 'Semester')
        self.plans = form_plans(all_plan)
        print(self.plans)

if __name__=='__main__':
	unittest.main()
