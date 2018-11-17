# Author    : Isuru Udukala (iudukala@gmail.com)
#

import os.path
import pprint

import regex_handler
from entities import Student, CourseInstance, UnitInstance
from regex_handler import data, everything_upto, progress_upto
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
        self.automatic_units = []
        self.planned_units = []
        self.attempted_units = []

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
            versions_list = [version.lower().replace("v. ", "") for version in versions_list if version is not ""]
            courses_list = [course for course in courses_list if course is not ""]

            # adding courses to attribute courses list
            for index in range(len(courses_list)):
                self.courses.append(CourseInstance(courses_list[index], versions_list[index]))

            # remove the processed section from the report text
            self.report_text = regex_handler.strip_match(self.report_text, regex_next_course, repl_count=1)

            # process the "automatic credit" and "recognition of prior learning" sections
            self.process_automatic_or_recognition()

            # process the "planned and completed componenets" section
            self.process_planned_and_completed_components()

    def process_automatic_or_recognition(self):
        """
        this handles the sections titled "automatic credit" and "recognition for prior learning". both these sections
        have the same format of information to be parsed and as such is handled by the same method.
        since the "automatic credit" section comes first on curtin's progress reports, this section is handled first.
        once that's processed, this method is recursively called once more to handle the section which comes after,
        which is "recognition for prior learning"; which may or may not be empty
        :return: None. the report text which is stored as an attribute is read and modified in place
        """
        # progress upto "automatic credits" section or "recognition of prior learning" section, whichever comes first
        self.report_text = progress_upto(self.report_text, everything_upto['automatic_or_recognition'])

        # check whether the report is currently at "automatic credits"
        section_is_automatic_credit = regex_handler.check_report_is_at_automatic_credit(self.report_text)

        # check whether the report is currently at "recognition of prior learning"
        section_is_recognition = regex_handler.check_report_is_at_recognition_of_prior_learning(self.report_text)

        # if "recognition of prior learning" section is empty, skip it and move to the
        # "planned and completed components" section
        if not (section_is_recognition & regex_handler.check_recognition_of_prior_is_empty(self.report_text)):
            # at this point, the leading entry in the report text and as such the section being processed by the parse
            # must either be "automatic credits" or "recognition of prior learning"
            if not (section_is_automatic_credit | section_is_recognition):
                raise ParseFailure("section is neither 'automatic credits' nor 'recognition of prior learning'")

            # grabbing the next set of unit IDs, credits and versions
            fetchedunits = regex_handler.grab_next_unit_ids(self.report_text)
            fetchedcredits = regex_handler.grab_next_credits(self.report_text)
            fetchedversions = regex_handler.grab_next_versions(self.report_text)

            for i in range(len(fetchedunits)):
                auto_unit = UnitInstance(fetchedunits[i], fetchedversions[i], fetchedcredits[i])
                self.automatic_units.append(auto_unit)

            # if the parser is currently at the "automatic credit" section, advance the report text to the next section,
            # which is recognition of prior learning" and then make a recursive call to this same function so that it
            # can be processed
            if section_is_automatic_credit:
                self.report_text = progress_upto(self.report_text, everything_upto['recognition_of_prior_learning'])
                self.process_automatic_or_recognition()

    def process_planned_and_completed_components(self):
        # progress to the "planned and completed components" section
        self.report_text = progress_upto(self.report_text, everything_upto['next_semester'])

        # grabbing the next set of unit IDs, credits and versions
        fetchedunits = regex_handler.grab_next_unit_ids(self.report_text)
        fetchedcredits = regex_handler.grab_next_credits(self.report_text)
        fetchedversions = regex_handler.grab_next_versions(self.report_text)
        fetchedstatuses = regex_handler.grab_next_unit_statuses(self.report_text)

        for i in range(len(fetchedunits)):
            unit = UnitInstance(fetchedunits[i], fetchedversions[i], fetchedcredits[i], unit_status=fetchedstatuses[i])
            if unit.is_planned():
                self.planned_units.append(unit)
            # if the unit has already been attempted, increment the value of attempt by 1 to reflect that
            elif unit in self.attempted_units:
                self.attempted_units[self.attempted_units.index(unit)].increment_attempt()
            else:
                self.attempted_units.append(unit)

    def __str__(self):
        def print_heading(heading):
            return "\n\n" + heading + " : \n" + "-" * 100 + "\n"

        output = "Report date\t\t: " + self.report_date
        output += "\nSanction status\t: {}".format(self.sanction_reason)
        output += print_heading("Student") + str(self.student)
        output += print_heading("Courses") + pprint.pformat(self.courses, indent=3)
        output += print_heading("Automatically credited units") + pprint.pformat(self.automatic_units, indent=3)
        output += print_heading("Planned units") + pprint.pformat(self.planned_units, indent=3)
        output += print_heading("Attempted units") + pprint.pformat(self.attempted_units, indent=3)

        return output + "\n\n"


def fetch_pdf_list():
    # return glob.glob("*/**/*.pdf")
    # return ['parser_tests/singlepage.pdf']
    return ["parser_tests/test_inputs/XiMingWong-pr.pdf", "parser_tests/test_inputs/Campbell-pr.pdf",
            "parser_tests/test_inputs/DUMMY - Sanction - BSc.pdf", "parser_tests/test_inputs/AAAAAAAEugene-pr copy.pdf"]

    # return ["parser_tests/test_inputs/AAAAAAAEugene-pr copy.pdf"]
    # return ['parser_tests/dummy_reports/Term - Stream Not Expanded.pdf']
    # return ["parser_tests/test_inputs/XiMingWong-pr.pdf"]
    # return ["parser_tests/test_inputs/Eugene-pr.pdf"]
    # return ["parser_tests/test_inputs/ChienFeiLin-pr.pdf"]


class ParseFailure(Exception):
    def __init__(self, message):
        super().__init__(message)


def main():
    for filepath in fetch_pdf_list():
        report = ReportParser(PDFMinerWrapper(filepath).parse_data())
        report.parse()

        print(report)


main()
