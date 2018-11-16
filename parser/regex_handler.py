# Author    : Isuru Udukala (iudukala@gmail.com)


import glob
import re
import collections

from wrapper import PDFMinerWrapper

# dictionary containing regular expressions. "per_page" in the identifier key in the dictionary in certain entries
# is used to identify the regexes that are supposed to exist per page ot make debugging easier

garbage = collections.OrderedDict({
    # garbage at start of page
    #

    # eg : Curtin University Student Progress Report Student One As At 21 Feb 2017
    'garbage_per_page_file_start':
        re.compile(
            r'curtin\s*university\s*student\s*progress\s*report\s*student\s*one\s*as\s*at\s*\d+\s*[a-z]+\s*\d+\s*',
            re.IGNORECASE),

    # garbage at the end of the page
    #

    # eg : Page 1 of 3
    'garbage_per_page_page_number':
        re.compile(r"page\s*\d+\s*of\s*\d+\s*", re.IGNORECASE),

    # eg : 12:53:30PM
    'garbage_per_page_timestamp':
        re.compile(r"\d{1,2}:\d{1,2}:\d{1,2}\s*(?:am|pm)", re.IGNORECASE),

    # [CuS1PG010j]
    'garbage_per_page_report_id_1':
        re.compile(r"^\[[a-z0-9]{10}\]$(?=[\s\S]*?^[0-9]{6}[a-z]$)", re.IGNORECASE | re.MULTILINE),
    #     re.compile(r"^\[[a-z0-9]{10}\]$", re.IGNORECASE | re.MULTILINE),

    # 212311I
    'garbage_per_page_report_id_2':
        re.compile(r"^\d{6}[a-z]$", re.IGNORECASE | re.MULTILINE),

    # eg : Total number of credits for course completion: 1000.0
    'garbage_credits_for_course_completion':
        re.compile(r"total\s*number\s*of\s*credits\s*for\s*course\s*completion\s*:\s*\d+(\.\d+)?", re.IGNORECASE),

    # eg : Total number of credits completed: 325.0
    'garbage_credits_completed':
        re.compile(r"total\s*number\s*of\s*credits\s*completed\s*:\s*\d+(\.\d+)?", re.IGNORECASE),

    # Default Location: Bentley Campus
    'garbage_default_location':
        re.compile(r"^default location\s?:\s?[\w\-\s]+$", re.IGNORECASE | re.MULTILINE)
})

data = {
    # group 1 : student ID
    # group 2 : student name
    'student_id_name':
        re.compile(r"student id\s?:\s*(\d{8})\s*student name\s?:\s*([\w ]*)", re.DOTALL | re.IGNORECASE),

    # group 1 : course ID
    # group 2 : course version
    'first_course_on_page':
        re.compile(
            r"^course\s?:\s*^(\d{6}|[a-z]+-[a-z]+)\s*^v.\s?(\d)\s*attempt\s?:\s?\d[\s\S]*?(?=^\d{6}|^[a-z]+-[a-z]+)",
            re.MULTILINE | re.IGNORECASE),

    # courses that come after the first course line. matched as groups of
    # [coursecollection]
    # [versioncollection]
    # group 1 : multiple lines of courses
    # group 2 : multiple lines of versions
    'next_courses':
        re.compile(r"((?:(?!^F-IN)(?<!^course:\s\n\n)^(?:[a-z]+-[a-z]+|[0-9]{6})$\n)+)\s*((?:^v.\s?\d{1,2}$\n)+)",
                   re.MULTILINE | re.IGNORECASE)

}

progress_upto_regexes = {
    'recognition_of_prior_learning':
        re.compile(r"[\s\S]*?(?=^recognition of prior learning$)", re.MULTILINE | re.IGNORECASE)
}


def progress_upto(text, progup_regex) -> str:
    """
    progresses upto certain points of the report by removing all irrelevant text before that point, leaving the parsed
    report data starting with the next section of relevant text so that the next section of the parser con continue
    from that point onwards. this function is in essence just a wrapper around the function strip_match() but exists
    for the sake of (hopefully) increasing readability of the code
    :param text: the parsed report text
    :param progup_regex: regular expression that specifies the location upto which the text should be trimmed to
                         (achieved through the use of lookaround assertions)
    :return: the parsed report text progressed upto the required point
    """
    return strip_match(text, progup_regex, repl_count=1)


def remove_garbage(text) -> str:
    for rgx_garbage in garbage.values():
        text = rgx_garbage.sub("", text)
    # removing newlines or spaces at the start of report data
    text = re.sub(r"^\s*|\s*$", "", text)

    return text


def strip_match(text, regex, repl_count=0) -> str:
    """
    removes the text matched by the passed regex repl_count times
    :param text: the text to be transformed
    :param repl_count: maximum number of replacements to be made. passed to re.sub() as the 'count' argument
    if an arg is passed to this function. if not, no arg is passed to re.sub(), ensuring all occurrences are
    replaced
    :param regex: compiled regular expression object to be matched and stripped from the text (report data)
    :return: None. Modifies the instance attribute report_text
    """
    text = regex.sub("", text, count=repl_count)
    # removing newlines or spaces at the start of report data
    text = remove_spaces(text)

    return text


def remove_spaces(text):
    """
    removes the spaces at the start of the line and at the end of the line. eg: if a line is
    <space><char1><space><char2><space>\n, it gets transformed to:
    <char1><space><char2>\n
    additionally removes spaces and newlines from the start and end of the text. (the full text, not individual lines)
    :param text: text to be transformed
    :return: the transformed text
    """
    starting_trailing_spaces = re.compile(r"^[ ]+|[ ]+$", re.MULTILINE)
    text = starting_trailing_spaces.sub("", text)

    text = re.sub(r"^\s*|\s*$", "", text)

    return text


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


def print_regex_groups(regex, garbage_remove=False):
    print("\n\nGroups for regex {} :".format(regex))

    for filepath in fetch_all_files():
        pdffile = PDFMinerWrapper(filepath).parse_data()
        pdftext = pdffile.text
        if garbage_remove is True:
            pdftext = remove_garbage(pdftext)

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
    # return ["parser_tests/test_inputs/XiMingWong-pr.pdf", "parser_tests/test_inputs/Campbell-pr.pdf"]
