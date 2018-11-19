# Author    : Isuru Udukala (iudukala@gmail.com)
#

import pprint

from core_app.parser import regex_handler
from core_app.parser.entities import Student, CourseInstance, UnitInstance
from core_app.parser.regex_handler import data_capture_regex, match_everything_upto, progress_upto
from core_app.parser.wrapper import PDFMinerWrapper


class ReportParser:
    def __init__(self, pdffile):
        self.pdffile = pdffile
        self.report_text = self.pdffile.text
        self.cleaned_text = self.pdffile.text

        self.report_date = None

        self.student = None
        self.courses = []
        self.automatic_units = []
        self.planned_units = []
        self.attempted_units = []

    def parse(self):
        # capturing report date
        self.report_date = regex_handler.garbage['per_page_file_start_and_date']. \
            match(self.report_text).group(1)

        # removing garbage lines from report text
        self.report_text = regex_handler.remove_garbage(self.report_text)
        # saving garbage removed text to cleaned_text to assist debugging
        self.cleaned_text = self.report_text

        # parsing student details
        self.process_student_details()

        # check if report text has a course section to parse, if it does, repeat process
        while regex_handler.check_course_section_exists(self.report_text):
            # parsing the course details section
            self.process_course_section()

            # process the "automatic credit" and "recognition of prior learning" sections
            self.process_section_automatic_or_recognition()

            # process the "planned and completed components" section
            self.process_section_planned_completed()

    def process_student_details(self):
        """
        captures student details (name, ID and sanction details) and constructs a 'Student' object and then removes
        that information from the report text
        :return: None. attributes are modified in place
        """
        # collecting student data
        student_regex = data_capture_regex['student_id_name']
        student_match = student_regex.search(self.report_text).groups()
        self.student = Student(student_match[0], student_match[1])
        self.report_text = regex_handler.strip_match(text=self.report_text, regex=student_regex)

        # checking if student has a sanction
        regex_sanction = data_capture_regex['sanction']
        sanction_match = regex_sanction.match(self.report_text)
        if sanction_match is not None:
            self.student.student_sanction = sanction_match.group(1)
        self.report_text = regex_handler.strip_match(self.report_text, regex_sanction, repl_count=1)

    def process_course_section(self):
        """
        fetch details of courses and constructs CourseInstance objects that are stored as attributes in the
        ReportParser object
        :return: None. report text is modified in place
        """

        # progress the report text to the line "Course:" if it's not already there
        self.report_text = progress_upto(self.report_text, match_everything_upto['course'])

        # collecting course data from the first line that contains a course
        regex_first_course = data_capture_regex['first_course_in_section']
        match_first_course = regex_first_course.search(self.report_text).groups()
        self.courses.append(CourseInstance(match_first_course[0], match_first_course[1]))
        # self.report_text = regex_handler.strip_match(self.report_text, regex_first_course, repl_count=1)

        # collecting courses from the lines after the line containing the first course id and name
        regex_next_course = data_capture_regex['next_courses']
        match_next_course = regex_next_course.search(self.report_text)
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

    def process_section_automatic_or_recognition(self):
        """
        handles the sections "automatic credit" and "recognition for prior learning". both sections specify units
        in the same format, and therefor is possible to parse in the same manner.
        since the "automatic credit" section comes first on curtin's progress reports, this section is handled first if
        it exists. once it's processed, this method calls itself after advancing the report text to the next section
        ("recognition for prior learning") which may or may not be empty

        the parser starts by progressing the report text to the start of the line "RECOGNITION OF PRIOR LEARNING" or
        "Automatic credit" and then reads the unit IDs in blocks within that section if the section exists. Once a
        block of unit IDs are read, the report text is progressed to that point. ie. all text leading upto (including
        the block of unit IDs) are removed from the report text.
        the removal of other fields (credits, versions) follow a much more conservative approach in which a record
        (whether it be a credit amount for a unit (25.0, 12.5) or a version (1, 2) is only removed if it has been
        added under it's related Unit ID

        :return: None. the report text which is stored as an attribute is read and modified in place
        """
        # resetting positional flags since this function is repeatedly called
        section_is_recognition = False
        section_is_automatic_credit = False

        # progress upto "automatic credits" section or "recognition of prior learning" section, whichever comes first
        self.report_text = progress_upto(self.report_text, match_everything_upto['automatic_or_recognition'])

        # check whether the report is currently at "automatic credits"
        section_is_automatic_credit = regex_handler.check_report_is_at_automatic_credit(self.report_text)

        # check whether the report is currently at "recognition of prior learning"
        section_is_recognition = regex_handler.check_report_is_at_recognition_of_prior_learning(self.report_text)

        # if "recognition of prior learning" section is empty, skip it and move to the "planned and completed
        # components" section
        if not (section_is_recognition & regex_handler.check_recognition_of_prior_is_empty(self.report_text)):
            # at this point, the leading entry in the report text and as such the section being processed by the parse
            # must either be "automatic credits" or "recognition of prior learning"
            if not (section_is_automatic_credit | section_is_recognition):
                raise ParseFailure("section is neither 'automatic credits' nor 'recognition of prior learning'")

            self.parse_unit_data("AUTO")

            # if the parser is currently at the "automatic credit" section, advance the report text to the next section,
            # which is recognition of prior learning" and then make a recursive call to this same function so that it
            # can be processed
            if section_is_automatic_credit:
                self.report_text = progress_upto(self.report_text,
                                                 match_everything_upto['recognition_of_prior_learning'])
                self.process_section_automatic_or_recognition()

    def process_section_planned_completed(self):
        """
        this method processes the section "Planned and completed components". it starts by progressing the report text
        to the start of the first semester header (eg: 2012 Semester 2) in the report text and then reading the
        unit IDs in blocks within that section. Once a block of unit IDs are read, the report text is progressed to
        that point. ie. all text leading upto (including the block of unit IDs) are removed from the report text.
        the removal of other fields (credits, versions, statuses) follow a much more conservative approach in which a
        record (whether it be a credit amount for a unit (25.0, 12.5) or a version (1, 2) or a unit status (PASS, FAIL,
        WD) is only removed if it has been added under it's related Unit ID
        :return:
        """
        # progress to the next semester section if one exists in the current course
        self.report_text = progress_upto(self.report_text, match_everything_upto['next_semester'])

        self.parse_unit_data("PlANNED")

        if not regex_handler.check_current_semester_is_last_in_course(self.report_text):
            self.process_section_planned_completed()
        else:
            return

    def parse_unit_data(self, mode):
        planned = mode.lower() == "planned"

        # grabbing the next set of unit IDs, credits and versions and then removing them from the text

        # fetchedunits = regex_handler.grab_next_unit_ids(self.report_text)
        self.report_text, fetchedunits = regex_handler.grab_remove_next_unit_ids(self.report_text)
        fetchedcredits = regex_handler.grab_next_credits(self.report_text)
        fetchedversions = regex_handler.grab_next_versions(self.report_text)

        fetchedstatuses = []
        if planned:
            fetchedstatuses = regex_handler.grab_next_unit_statuses(self.report_text)

        for i in range(len(fetchedunits)):
            # reading common fields and removing them from the text
            unit_id = fetchedunits[i]
            # self.report_text = regex_handler.remove_first_instance_of(unit_id, self.report_text)

            unit_credits = fetchedcredits[i]
            self.report_text = regex_handler.remove_first_instance_of(unit_credits, self.report_text)

            unit_version = fetchedversions[i]
            self.report_text = regex_handler.remove_first_instance_of(unit_version, self.report_text)

            unit_status = None
            if planned:
                unit_status = fetchedstatuses[i]
                self.report_text = regex_handler.remove_first_instance_of(unit_status, self.report_text)

            unit_attempt = 1
            if not planned:
                unit_attempt = None

            parsed_unit = UnitInstance(unit_id=unit_id, unit_version=unit_version, unit_credits=unit_credits,
                                       unit_status=unit_status, unit_attempt=unit_attempt)

            if planned:
                if parsed_unit.is_planned():
                    self.planned_units.append(parsed_unit)
                # if the unit has already been attempted, update the units and increment the value of 'attempt'
                # by 1 to reflect that
                elif parsed_unit in self.attempted_units:
                    cur_attempt_val = self.attempted_units[self.attempted_units.index(parsed_unit)].unit_attempt
                    parsed_unit.unit_attempt = cur_attempt_val
                    parsed_unit.increment_attempt()

                    # updating the unit in the report
                    self.attempted_units[self.attempted_units.index(parsed_unit)] = parsed_unit
                else:
                    self.attempted_units.append(parsed_unit)
            else:
                self.automatic_units.append(parsed_unit)

    def __str__(self):
        def print_seperator():
            return "-" * 100 + "\n"

        def print_section(heading, data_list, strout_indent=3):
            strout = "\n\n{} : [{} records]\n".format(heading, len(data_list))
            strout += print_seperator()
            strout += pprint.pformat(data_list, indent=strout_indent) + "\n"
            return strout

        output = "\nReport date\t\t: {}\n\n".format(self.report_date)
        output += "Student : \n{}{}".format(print_seperator(), str(self.student))

        output += print_section("Courses", self.courses)
        output += print_section("Automatically credited units", self.automatic_units)
        output += print_section("Planned units", self.planned_units)
        output += print_section("Attempted units", self.attempted_units)

        return output + "\n"

    def __repr__(self):
        return self.__str__()

    def parser_output_summary(self) -> str:
        output = "\nPARSED DATA SUMMARY for [{}, {}]\n{}\n".format(self.student.student_name,
                                                                   self.student.student_id,
                                                                   "-" * 100)
        output += "Courses\t\t\t: {}\n".format(len(self.courses))
        output += "Automatic units\t: {}\n".format(len(self.automatic_units))
        output += "Attempted units\t: {}".format(len(self.attempted_units))

        return output

    def format_report(self):
        """
        collates information into a dictionary object in the format accepted by the system
        :return: 
        """
        # if the report object has not been parsed output None
        if self.report_date is None:
            return None

        from collections import OrderedDict
        report_dictionary = {'date': self.report_date,
                             'name': self.student.student_name,
                             'id': self.student.student_id}

        # courses under key 'courses'
        courses_dict = OrderedDict()
        for course in self.courses:
            courses_dict[course.course_id] = course.course_version
        report_dictionary['course'] = courses_dict

        # planned units under key 'planned'
        planned_dict = {}
        for unit in self.planned_units:
            planned_dict[unit.unit_id] = {
                'credits': unit.unit_credits,
                'status': unit.unit_status,
                'ver': unit.unit_version
            }
        report_dictionary['planned'] = planned_dict

        # automatically credited units under key 'automatic'
        automatic_dict = {}
        for unit in self.automatic_units:
            automatic_dict[unit.unit_id] = {
                'ver': unit.unit_version,
                'credits': unit.unit_credits,
            }
        report_dictionary['automatic'] = automatic_dict

        # attempted units under key 'units'
        attempted_dict = {}
        for unit in self.attempted_units:
            attempted_dict[unit.unit_id] = {
                'status': unit.unit_status,
                'ver': unit.unit_version,
                'credits': unit.unit_credits,
                'attempt': unit.unit_attempt
            }
        report_dictionary['units'] = attempted_dict

        # pprint.pformat(report_dictionary, indent=3, width=90)
        return report_dictionary


def fetch_pdf_list():
    import os.path
    pdfdir = os.path.join("parser_tests", "test_inputs")
    pdflist = [
        "XiMingWong-pr.pdf",
        "Eugene-pr.pdf",
        "ChienFeiLin-pr.pdf",
        "Campbell-pr.pdf",
        "Steven-pr.pdf",
        "Yoakim-pr.pdf",
        "Darryl-pr.pdf",
    ]
    pdflist = [os.path.join(pdfdir, file) for file in pdflist]

    return pdflist


class ParseFailure(Exception):
    def __init__(self, message):
        super().__init__(message)


def main():
    for filepath in fetch_pdf_list():
        try:
            with open(filepath, "rb") as file:
                report = ReportParser(PDFMinerWrapper(file).parse_data())
                report.parse()

                print(report)
                print(report.parser_output_summary())
        except:
            print("\nParsing failed for file : " + filepath)


def parse_progress_report(fp):
    try:
        raw_pdf_data = PDFMinerWrapper(fp).parse_data()
        report = ReportParser(raw_pdf_data)
        report.parse()

        return report.format_report()
    except:
        return None


if __name__ == "__main__":
    main()
