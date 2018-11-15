# Author    : Isuru Udukala (iudukala@gmail.com)


import glob
import re

from wrapper import PDFMinerWrapper

# dictionary containing regular expressions. "per_page" in the identifier key in the dictionary in certain entries
# is used to identify the regexes that are supposed to exist per page ot make debugging easier

garbage = {
    # garbage at start of page
    # eg : Curtin University Student Progress Report Student One As At 21 Feb 2017
    'garbage_per_page_file_start':
        re.compile(
            r'curtin\s*university\s*student\s*progress\s*report\s*student\s*one\s*as\s*at\s*\d+\s*[a-z]+\s*\d+\s*',
            re.IGNORECASE),

    # garbage at the end of the page
    # eg : Page 1 of 3
    'garbage_per_page_page_number':
        re.compile(r"page\s*\d+\s*of\s*\d+\s*", re.IGNORECASE),

    # eg : 12:53:30PM
    'garbage_per_page_timestamp':
        re.compile(r"\d{1,2}:\d{1,2}:\d{1,2}\s*(?:am|pm)", re.IGNORECASE),

    # [CuS1PG010j]
    'garbage_per_page_report_id_1':
    #     re.compile(r"^\[[a-z0-9]{10}\]$(?=[\s\S]*?^[0-9]{6}[a-z]$)|^\d{6}[a-z]$", re.IGNORECASE | re.MULTILINE),
        re.compile(r"^\[[a-z0-9]{10}\]$", re.IGNORECASE | re.MULTILINE),

    # 212311I
    'garbage_per_page_report_id_2':
        re.compile(r"^\d{6}[a-z]$", re.IGNORECASE | re.MULTILINE),

    # eg : Total number of credits for course completion: 1000.0
    'garbage_credits_for_course_completion':
        re.compile(r"total\s*number\s*of\s*credits\s*for\s*course\s*completion\s*:\s*\d+(\.\d+)?", re.IGNORECASE),

    # eg : Total number of credits completed: 325.0
    'garbage_credits_completed':
        re.compile(r"total\s*number\s*of\s*credits\s*completed\s*:\s*\d+(\.\d+)?", re.IGNORECASE),
}

data = {
    'student_id_name':
        re.compile(r"student id\s?:\s*(\d{8})\s*student name\s?:\s*([\w ]*)", re.DOTALL | re.IGNORECASE)}


def check_regex_match(regex_list):
    """
    checks the progress reports in the parser_tests/ dir to see if there exists matches for a particular
    regular expression
    :param regex_list: list containing compiled regular expressions to check for
    :return: None
    """
    for rgx in regex_list:
        print("\n\nmatches for regex {} :".format(rgx))
        for filepath in fetch_all_files():
            pdffile = PDFMinerWrapper(filepath).parse_data()
            pdftext = pdffile.text
            regex_match_count = len(rgx.findall(pdftext))
            if regex_match_count == pdffile.page_count:
                print("\tP", end="")
            elif regex_match_count > 0:
                print("\t+", end="")
            else:
                print("\t-", end="")
            print("\tfound {} matches in {} pages in file [{}]".
                  format(regex_match_count, pdffile.page_count, pdffile.file_name))
            for index, rgx_match in enumerate(rgx.findall(pdftext)):
                transformed_text = re.sub(r"\n+", '\t' * 3, rgx_match)
                print("\t\t\t{}.\t{}".format(index, transformed_text))


def print_regex_groups(regex):
    print("\n\nGroups for regex {} :".format(regex))

    for filepath in fetch_all_files():
        pdffile = PDFMinerWrapper(filepath).parse_data()
        pdftext = pdffile.text

        regex_match_count = len(regex.findall(pdftext))
        print("\t{} matches in file [{}] : ".format(regex_match_count, pdffile.file_name))
        for index, regex_group in enumerate(regex.findall(pdftext)):
            print("\t\t{}:\t{}".format(index, regex_group))



        # print(regex.search(pdftext).group(1))
        # print(regex.group)
        # regex.group()
        # matches = regex.findall(pdftext)
        # matches = re.match(regex, pdftext)
        # print(matches)

        # print(regex)
        # for index, group in enumerate(re.match(regex, pdftext).groups()):
        #     print(group)



def fetch_all_files():
    return glob.glob("*/**/*.pdf")
