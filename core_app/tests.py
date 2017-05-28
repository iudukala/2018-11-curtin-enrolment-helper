from django.test import TestCase
from core_app.models import Course, CourseTemplate, CourseTemplateOptions, Student, StudentUnit, Unit
from core_app.views import form_templates, form_plans, form_course

# Create your tests here.

###################################
# Unit Test for CourseProgress
###################################
class TestCourseProgress(TestCase):

    def setUp(self):
		# the test set will use below student ID as default
        student_id = 16102183

        # Course
        Course.objects.create(CourseID='7777', Name='SE', Version='2B', TotalCredits=600)

        # Student
        Student.objects.create(StudentID=16102183, Name='Chen', CreditsCompleted=500, AcademicStatus=1, CourseID='7777')

        # Course Temp
        CourseTemplate.objects.create(CourseID='7777', Option=163)


        # Course Temp Units
        CourseTemplateOptions.objects.create(UnitID=123456, Option=163, Year=1, Semester=1)


        # Student Plan Units
        StudentUnits.objects,create(StudentID=16102183, UnitID=123456, Attempts=1, Status='1', prerequisiteAchieved=True, Year=1, Semester=1)


        # UNITS
        Unit.objects.create(UnitID=123456, UnitCode='abc123', Name='OOSE', Version='100', Semester=1, Credits=25.0)


    def test_templates_dict(self):
        student = Student.objects.get(pk=student_id)
        course = Course.objects.get(CourseID=student.CourseID)
        all_course_temp = CourseTemplate.objects.all().filter(CourseID=course.CourseID)
        self.form_templates(all_course_temp, student_id)

    def test_plans_dict(self):
        student = Student.objects.get(pk=student_id)
        all_plan = StudentUnit.objects.all().filter(StudentID=student.StudentID).order_by('Year', 'Semester')
        self.plans = form_plans(all_plan)


if __name__=='__main__':
	unittest.main()
