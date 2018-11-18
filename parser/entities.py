# Author    : Isuru Udukala (iudukala@gmail.com)


class Student:
    def __init__(self, student_id, student_name):
        self.student_id = str(student_id).strip()
        self.student_name = str(student_name).strip()
        self.student_progress = {}
        self.student_sanction = None

    def __str__(self):
        return "Student name\t: [{}]\nStudent ID\t\t: [{}]\nSanction\t\t: {}".\
            format(self.student_name, self.student_id, self.student_sanction)

    def __repr__(self):
        return self.__str__()


class CourseInstance:
    def __init__(self, course_id, course_ver):
        self.course_id = str(course_id).strip()
        self.course_version = str(course_ver).strip()

    def __str__(self):
        return "Course ID\t\t: [{}]\tCourse version\t: [{}]".format(self.course_id, self.course_version)

    def __repr__(self):
        return self.__str__()


class UnitInstance:
    def __init__(self, unit_id, unit_version, unit_credits, unit_status=None, unit_attempt=1):
        self.unit_id = str(unit_id).strip()
        self.unit_version = str(unit_version).strip()
        self.unit_credits = str(unit_credits).strip()

        self.unit_status = None
        if unit_status is not None:
            self.unit_status = str(unit_status).strip()

        self.unit_attempt = None
        if unit_attempt is not None:
            self.unit_attempt = int(unit_attempt)

    def is_planned(self) -> bool:
        return (self.unit_status == "PLN") | (self.unit_status == "ENR")

    def increment_attempt(self):
        self.unit_attempt += 1

    def __eq__(self, other):
        iseq = self.unit_id == other.unit_id
        return iseq

    # todo handle none values in mark and status properly
    def __str__(self):
        strout = "[{}]\t\t:\tVersion : [{}]\tCredits : [{}]".format(self.unit_id, self.unit_version, self.unit_credits)
        if self.unit_status is not None:
            strout += "\tStatus : [{}]".format(self.unit_status)
        if self.unit_attempt is not None:
            strout += "\t\tAttempt : [{}]".format(self.unit_attempt)

        return strout

    def __repr__(self):
        return self.__str__()
