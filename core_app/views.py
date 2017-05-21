from .models import Student, StudentUnit, CourseTemplate
from django.http import JsonResponse
import json


student_id = -1
# If all good then add units to completedUnits array waiting to save
valid_enrol_units = []
def enrol_plan_validity(request):
    if student_id is not -1 AND request.is_ajax():
        try:
            received_plan_json = json.loads(request.body.decode('utf-8'))
        except Student.DoesNotExist:
            raise RuntimeError('errors: can not parse json object') from error
        try:
            boolean_respond = validity_query(received_plan_json)
        except Student.DoesNotExist:
            raise RuntimeError('') from error
    else:
        raise Http404()


def validity_query(received_plan_json):
    for key, value in received_plan_json.items():
        year = key
        sem_value = value
        for key, value in sem_value.items():
            sem = Key
            unit_value = value
            credits_this_semester = 0
            for key, value in unit_value.items():
                unit_id = Key
                unit_info = Value

                if unit_id is not 'ELECTIVE'
                    completed_unit = StudentUnits.objects.get(StudentID=student_id AND UnitID=unit_id)
                    # this is course temp object
                    if not completed_unit
                        # check the unit if belongs to this course
                        option = CourseTemplateOptions.objects.get(UnitID=unit_id)
                        unit_course_id = CourseTemplate.objects.get(Option=option)
                        student_course_id = Courses.objects.get(StudentID=student_id)
                        if student_course_id is not unit_course_id
                            # check equalence if this unit is a equivalence unit
                            # if ..
                                # return False

                        # check prerequisites true or false true go next
                        option = CourseTemplateOptions.objects.get(UnitID=unit_id)
                        prerequisite_units = Prerequisite.objects.all().filter(Option=option)
                        for unit in prerequisite_units:
                            a_unit = StudentUnits.objects.get(UnitID=unit.UnitID)
                            if not StudentUnits.objects.get(UnitID=unit.UnitID)
                                return False
                            elif a_unit.PrerequisiteAchieved is False or a_unit.Status is 3 or a_unit.Status is 1 or a_unit.Year is not year or a_unit.Semester is not sem
                                return False
                        # add credits
                    else
                        # here will need to generate an error message to denote what problems are with enrollment (elif)
                        if completed_unit.Status is 2 or completed_unit.Year is not year or completed_unit.Semester is not sem
                            del valid_enrol_units[:]
                            return False
                        else
                            credits_this_semester += unit_info['credits']
                            valid_enrol_units.append(unit)
                # unit is elective
                else
                    credits_this_semester += unit_info['credits']

            # Credit amount  per semester musn't exceed 100
            if credits_this_semester > 100
                del valid_enrol_units[:]
                return False
