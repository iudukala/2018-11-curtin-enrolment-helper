from .models import Student, StudentUnit, CourseTemplate, CourseTemplateOptions, Units, Equivalence, Prerequisite, Options
import json



def enrol_plan_validity(request):
    # If all good then add units to completedUnits array waiting to save
    valid_enrol_units = []
    student_id = -1
    if student_id is not -1 and request.is_ajax():
        try:
            received_plan_json = json.loads(request.body.decode('utf-8'))
        except Student.DoesNotExist:
            raise RuntimeError('errors: can not parse json object') from error
        try:
            boolean_respond = validity_query(received_plan_json, valid_enrol_units, student_id)
        except Student.DoesNotExist:
            raise RuntimeError('') from error
    else:
        raise Http404()

    return boolean_respond



def validity_query(received_plan_json, valid_enrol_units, student_id):
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
                    # retrieve information related to this unit in student plan
                    completed_unit = StudentUnits.objects.get(StudentID=student_id AND UnitID=unit_id)
                    # retrieve information related to this unit in coursetempoption
                    course_temp_option = CourseTemplateOptions.objects.get(UnitID=unit_id)
                    # retrieve equivalence
                    equiv_unit = Equivalence.objects.get(UnitID=unit_id)
                    # this is course temp object
                    if not completed_unit
                        if course_temp_option.Year is not year and course_temp_option.Semester is not sem
                            del valid_enrol_units[:]
                            return False
                        # check if the equivalence already existed in the previous student plan and passed it
                        elif StudentUnits.objects.get(StudentID=student_id AND UnitID=equiv_unit).Status is 2
                            del valid_enrol_units[:]
                            return False
                        # checking prerequisite if it has been achieved
                        prerequisite = Prerequisite.objects.get(UnitID=unit_id)
                        prerequisite_units = Options.objects.all().filter(Option=prerequisite.Option)
                        for unit in prerequisite_units:
                            # if can not find the prerequisite unit in student plan that means does not enrol prerequisite before
                            if not StudentUnits.objects.get(UnitID=unit.UnitID)
                                del valid_enrol_units[:]
                                return False
                            # check the prerequisite if passed or failed in previous student plan
                            a_unit = StudentUnits.objects.get(UnitID=unit.UnitID)
                            if a_unit.Status is not 2
                                del valid_enrol_units[:]
                                return False
                            # if all good add this temp unit and add up credits
                            credits_this_semester += unit_info['credits']
                            valid_enrol_units.append(unit)

                    # this is previous plan unit
                    else
                        # here will need to generate an error message to denote what problems are with enrollment (elif)
                        if completed_unit.Status is 2 or course_temp_option.Year is not year or course_temp_option.Semester is not sem
                            del valid_enrol_units[:]
                            return False
                        else
                            credits_this_semester += unit_info['credits']
                            valid_enrol_units.append(unit)
                # unit is elective
                else
                    credits_this_semester += unit_info['credits']
            # Credit amount per semester musn't exceed 100
            if credits_this_semester > 100
                del valid_enrol_units[:]
                return False

    return True
