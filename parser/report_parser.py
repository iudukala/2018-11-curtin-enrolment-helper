# Author    : Isuru Udukala (iudukala@gmail.com)


import glob
import re


import regexes
from wrapper import PDFMinerWrapper
from entities import Student, CourseInstance, UnitInstance


class ReportParser:
    def __init__(self, pdffile):
        self.report_student = None
        self.pdffile = pdffile
        self.report_text = self.pdffile.text

    def parse(self):
        # removing garbage
        print("\n{} - {}".format(self.report_text.count("\n"), self.pdffile.file_name))

        with open("initial output.txt", "w") as filehandle:
            filehandle.write(self.report_text)

        for rgx_pat in regexes.garbage.values():
            self.strip_match(rgx_pat)

        print("{} - {}".format(self.report_text.count("\n"), self.pdffile.file_name))

        # collecting student data
        student_regex = regexes.data['student_id_name']
        student_match = student_regex.search(self.report_text).groups()
        self.report_student = Student(student_match[0], student_match[1])
        self.strip_match(student_regex)

        with open("final_output.txt", "w") as filehandle:
            filehandle.write(self.report_text)

    def strip_match(self, regex):
        """
        Returns the matched groups in the passed regex and
        :param regex: compiled regular expression object to be matched and stripped from the report data
        :return: None. Modifies the instance attribute report_text
        """
        self.report_text = regex.sub("", self.report_text)
        # removing newlines or spaces at the start of report data
        self.report_text = re.sub(r"^\s*", "", self.report_text)


def fetch_pdf_list():
    # return glob.glob("*/**/*.pdf")
    # return ['parser_tests/singlepage.pdf']
    # return ["parser_tests/test_inputs/Campbell-pr.pdf"]
    # return ['parser_tests/dummy_reports/Term - Stream Not Expanded.pdf']

    return ["parser_tests/test_inputs/Eugene-pr.pdf"]


def maintwo():
    # xr = re.compile(r"student id\s?:\s*(\d{8})\s*student name\s?:\s*([\w ]*)", re.IGNORECASE | re.DOTALL)
    # regexes.print_regex_groups(xr)
    # xr = regexes.garbage.get("garbage_per_page_page_number")
    # regexes.check_regex_match([xr])
    regex = regexes.garbage['garbage_per_page_report_id_1']
    # regex = re.compile(r"^\d{6}[a-z]$", re.IGNORECASE | re.MULTILINE)
    regexes.check_regex_match([regex])


def main():
    for filepath in fetch_pdf_list():
        pdffile = PDFMinerWrapper(filepath).parse_data()
        ReportParser(pdffile).parse()


main()
# regex_list = [regexes.garbage.get("garbage_per_page_report_id")]
# regexes.check_regex_match(regex_list)
# maintwo()



