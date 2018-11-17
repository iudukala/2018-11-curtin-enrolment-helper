# Author    : Isuru Udukala (iudukala@gmail.com)
#

import os.path
import pprint

import regex_handler
from entities import Student, CourseInstance
from regex_handler import data
from wrapper import PDFMinerWrapper

LOGGING_DIR = "Logging"


class ReportParser:
    def __init__(self, pdffile):
        self.pdffile = pdffile
        self.report_text = self.pdffile.text

        self.report_date = None

        # sanction flag and reason
        self.sanction = False
        self.sanction_reason = None

        self.student = None
        self.courses = []

    def parse(self):
        # capturing report date
        self.report_date = regex_handler.garbage['garbage_per_page_file_start_and_date']. \
            match(self.report_text).group(1)

        initial_outputlogname = os.path.join(LOGGING_DIR, self.pdffile.file_name + "_initial.txt")
        with open(initial_outputlogname, "w") as filehandle:
            filehandle.write(self.report_text)

        # removing garbage
        self.report_text = regex_handler.remove_garbage(self.report_text)

        # collecting student data
        student_regex = data['student_id_name']
        student_match = student_regex.search(self.report_text).groups()
        self.student = Student(student_match[0], student_match[1])
        self.report_text = regex_handler.strip_match(text=self.report_text, regex=student_regex)

        # checking if student has a sanction
        regex_sanction = data['sanction']
        sanction_match = regex_sanction.match(self.report_text)
        if sanction_match is not None:
            self.sanction = True
            self.sanction_reason = sanction_match.group(1)
        self.report_text = regex_handler.strip_match(self.report_text, regex_sanction, repl_count=1)

        self.process_course_section()

        final_outputlogname = os.path.join(LOGGING_DIR, self.pdffile.file_name + "_final.txt")
        with open(final_outputlogname, "w") as filehandle:
            filehandle.write(self.report_text)

    def process_course_section(self):
        # collecting course data from the first line that contains a course
        regex_first_course = data['first_course_on_page']
        match_first_course = regex_first_course.search(self.report_text).groups()
        self.courses.append(CourseInstance(match_first_course[0], match_first_course[1]))
        self.report_text = regex_handler.strip_match(self.report_text, regex_first_course, repl_count=1)

        # collecting courses from the lines after the line containing the first first course id and name
        regex_next_course = data['next_courses']
        match_next_course = regex_next_course.match(self.report_text)
        if match_next_course is not None:
            courses_list = match_next_course.group(1).splitlines(keepends=False)
            versions_list = match_next_course.group(2).splitlines(keepends=False)

            # transforming elements in versions_list in the courses in the lower lines from
            # [v. 1] to [1]
            for index in range(len(versions_list)):
                versions_list[index] = versions_list[index].lower().replace("v. ", "")

            # adding courses to attribute courses list
            for index in range(len(courses_list)):
                if courses_list[index] is not '':
                    self.courses.append(CourseInstance(courses_list[index], versions_list[index]))
            self.report_text = regex_handler.strip_match(self.report_text, regex_next_course, repl_count=1)

            self.handle_automatic_recognition_section()

    def handle_automatic_recognition_section(self):
        # progress upto 'automatic credits' section or 'recognition of prior learning' section
        self.report_text = regex_handler.progress_upto(
            self.report_text, regex_handler.progress_upto_regexes['automatic_or_recognition'])

        # grabbing the next set of unit IDs
        tempunits = regex_handler.grab_unit_ids(self.report_text)
        print(tempunits)
        # progress upto the next set of corresponding credits
        # self.report_text = regex_handler.progress_upto(self.report_text, regex_handler.progress_upto_regexes['unit_id_to_credits'])

    def __str__(self):
        output = "\n" * 2 + "Report date\t\t: " + self.report_date + "\n\n"
        output += str(self.student) + "\n" * 2
        output += "Sanction status\t: {}".format(self.sanction_reason) + "\n" * 2
        output += "Courses\t:\n"
        output += pprint.pformat(self.courses)
        output += "\n" + "-" * 150

        return output


def fetch_pdf_list():
    # return glob.glob("*/**/*.pdf")
    # return ['parser_tests/singlepage.pdf']
    return ["parser_tests/test_inputs/XiMingWong-pr.pdf",
            "parser_tests/test_inputs/Campbell-pr.pdf",
            "parser_tests/test_inputs/DUMMY - Sanction - BSc.pdf",
            "parser_tests/test_inputs/AAAAAAAEugene-pr copy.pdf"]
    # return ['parser_tests/dummy_reports/Term - Stream Not Expanded.pdf']
    # return ["parser_tests/test_inputs/XiMingWong-pr.pdf"]
    # return ["parser_tests/test_inputs/Eugene-pr.pdf"]
    # return ["parser_tests/test_inputs/ChienFeiLin-pr.pdf"]


def maintwo():
    # xr = re.compile(r"student id\s?:\s*(\d{8})\s*student name\s?:\s*([\w ]*)", re.IGNORECASE | re.DOTALL)
    # regexes.print_regex_groups(xr)
    # xr = regexes.garbage.get("garbage_per_page_page_number")
    # regexes.check_regex_match([xr])
    # regex = regex_handler.garbage['garbage_per_page_report_id_1']
    # regex = re.compile(r"^\d{6}[a-z]$", re.IGNORECASE | re.MULTILINE)
    # regex = re.compile(r'^([0-9, A-Z]+-)?[0-9, A-Z]{4,}$', re.IGNORECASE | re.MULTILINE)
    # regex = data['first_course_on_page']
    # regex = data['next_courses']
    # regex = regex_handler.situational_regexes['progress_upto']
    # regex = garbage['garbage_default_location']
    # regex_handler.print_regex_groups(regex, garbage_remove=True)
    regex = regex_handler.data['sanction']
    # regex_handler.check_regex_match([regex])
    regex_handler.print_regex_groups(regex)


def main():
    for filepath in fetch_pdf_list():
        report = ReportParser(PDFMinerWrapper(filepath).parse_data())
        report.parse()

        # print(report)


main()
# maintwo()
