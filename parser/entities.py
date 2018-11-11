class Student:
    def __init__(self, student_id, student_name):
        self.student_id = student_id
        self.student_name = student_name
        self.student_progress = {}

    def __str__(self):
        return "Student name\t: {}\nStudent ID\t: {}".format(self.student_name, self.student_id)


class CourseInstance:
    def __init__(self, course_id, course_ver, course_attempt):
        self.course_id = course_id
        self.course_version = course_ver
        self.course_attempt = course_attempt


class UnitInstance:
    def __init__(self, unit_id, unit_version, unit_credits, unit_mark=None, unit_status=None):
        self.unit_id = unit_id
        self.unit_version = unit_version
        self.unit_credits = unit_credits
        self.unit_mark = unit_mark
        self.unit_status = unit_status

# todo handle none values in mark and status properly
    def __str__(self):
        return "[{}]\n\tVersion\t: {}\n\tCredits\t: {}\n\tMark\t: {}\n\tStatus\t: {}"\
            .format(self.unit_id, self.unit_version, self.unit_credits, self.unit_mark, self.unit_status)
