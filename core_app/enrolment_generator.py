import json
# from .models import *
from .models import Student
from .models import Course
from .models import Unit
from .models import CourseTemplate
from .models import StudentUnit

#####
# {
#     template: {
#         <YEAR> : {
#         <SEMESTER> : {
#             <UNIT ID> : { name: <NAME>, credits: <CREDIT WORTH> }
#             }
#         }
#     }
#     plan: {
#         <YEAR> : {
#             <SEMESTER> : {
#                 <UNIT ID> : {
#                          name: <NAME>, credits: <CREDIT WORTH>, attempts: <PREV. ATTEMPTS>
#                 }
#             }
#         }
#     }
# }


class Enrolment_Generator():

    def __init__(self, in_id):

        self.student = self.get_student(in_id)
        self.plan = self.generate_plan(self.student)
        self.template = self.generate_template(self.student)
        self.complete = self.combine(self.plan, self.template)

    def get_student(self, in_id):
        student = Student.objects.get(StudentID=in_id)
        return student

    def generate_template(self, student):
        # Use CourseTemplate
        template = {'balh': 'blahblah'}
        all_course_templates = CourseTemplate.objects.all().filter(CourseID=student.CourseID)
        # all_course_templates = all_course_templates.values()
        # all_course_templates = all_course_templates
        # print(all_course_templates['17080170', '312649'])
        # print(all_course_templates)
        return template

    def generate_plan(self, student):
        all_student_units = StudentUnit.objects.all().filter(StudentID=student.StudentID)
        student_unit_dict = all_student_units.values()
        # print(student_unit_dict[0])
        # print(student_unit_dict.StudentID_id.values())

        # Use StudentUnit
        plan = {'id': '17080170'}
        return plan

    def combine(self, plan, template):
        combined = {
                'template': template,
                'plan':     plan
                }
        return combined

    def get_templates_and_plan(self):
        return json.dumps(self.complete)
