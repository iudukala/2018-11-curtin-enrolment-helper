from django.test import TestCase
from core_app.models import CourseTemplate, CourseTemplateOptions, StudentUnits, Units
from core_app.views import form_templates, form_plans


###################################
# Unit Test for CourseProgress
###################################
class TestCourseProgress(TestCase):

    def setUp(self):
		# the test set will use below student ID as default
		student_id = '16102183'

		# Student
		Student.objects.create(StudentID='', Name='', CreditsCompleted='', AcademicStatus='', CourseID='')

		# Course Temp
		CourseTemplate.objects.create(CourseID='', Option='')


		# Course Temp Units
		CourseTemplateOptions.objects.create(UnitID='', Option='', Year='', Semester='')


		# Student Plan Units
		StudentUnits.objects,create(StudentID='', UnitID='', Attempts-='', Status='', prerequisiteAchieved='', Year='', Semester='')


		# UNITS
		Unit.objects.create(UnitID='312649', UnitCode='', Name='', Version='', Semester='', Credits='')


	def test_templates_dict(self):
		student = Student.objects.get(pk=student_id)
		course_temp = CourseTemplate.objects.get(CourseID=student.CourseID)
		all_template_option = CourseTemplateOptions.objects.all().filter(Option=course_temp.Option)

		self.assertEqual()

	def test_plans_dict(self):
		student = Student.objects.get(pk=student_id)
		all_plan = StudentUnit.objects.all().filter(StudentID=student.StudentID)
		self.assertEqual()


if __name__=='__main__':
	unittest.main()
