# Author    : Isuru Udukala (iudukala@gmail.com)


class Student:
    def __init__(self, student_id, student_name):
        self.student_id = str(student_id).strip()
        self.student_name = str(student_name).strip()
        self.student_progress = {}

    def __repr__(self):
        return "Student name\t: [{}]\nStudent ID\t\t: [{}]".format(self.student_name, self.student_id)


class CourseInstance:
    def __init__(self, course_id, course_ver):
        self.course_id = str(course_id).strip()
        self.course_version = str(course_ver).strip()
        # self.course_attempt = course_attempt

    def __repr__(self):
        return "Course ID\t\t: [{}]\tCourse version\t: [{}]".format(self.course_id, self.course_version)


class UnitInstance:
    def __init__(self, unit_id, unit_version, unit_credits, unit_status=None, unit_attempt=1):
        self.unit_id = str(unit_id).strip()
        self.unit_version = str(unit_version).strip()
        self.unit_credits = str(unit_credits).strip()
        self.unit_status = str(unit_status).strip()
        self.unit_attempt = int(unit_attempt)

    def is_planned(self) -> bool:
        return (self.unit_status is "PLN") | (self.unit_status is "ENR")

    def increment_attempt(self):
        self.unit_attempt += 1

    def __eq__(self, other):
        iseq = self.unit_id is other.unit_id
        return iseq

    # todo handle none values in mark and status properly
    def __repr__(self):
        return "[{}]\t\t:\tVersion : [{}]\tCredits : [{}]\tStatus : [{}]\t\tAttempt : [{}]" \
            .format(self.unit_id, self.unit_version, self.unit_credits,  self.unit_status, self.unit_attempt)
