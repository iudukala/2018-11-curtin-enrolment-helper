# Author    : Isuru Udukala (iudukala@gmail.com)
#

import collections
import glob
import re

from wrapper import PDFMinerWrapper

# dictionary containing garbage regular expressions. "per_page" in the identifier key in the dictionary in certain
# entries is used to identify the regexes that are supposed to exist per page ot make debugging easier
garbage = collections.OrderedDict({
    # garbage at start of page
    #

    # eg : Curtin University Student Progress Report Student One As At 21 Feb 2017
    # group 1 : report date
    'garbage_per_page_file_start_and_date':
        re.compile(
            r'curtin\s*university\s*student\s*progress\s*report\s*'
            r'student\s*one\s*'
            r'as\s*at\s*(\d+\s*[a-z]+\s*\d+)\s*',
            re.IGNORECASE),

    'garbage_headers':
        re.compile(
            r"^spk\scd$|"
            r"^spk\stitle$|"
            r"^spk\sver$|"
            r"^type$|"
            r"^designated$|"
            r"^credit\sreceived$|"
            r"^grade$|"
            r"^mark$|"
            r"^general$|"
            r"^on\sstudy\splan\?$|"
            r"^status$|"
            r"^boe$|"
            r"^final$|"
            r"^credits$",
            re.MULTILINE | re.IGNORECASE),

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

raw_regexes = {
    'semester_sep':
        r"^not[\s]assigned[\s]to[\s]a[\s]specific[\s]year$|^\d{4}[ \t]*(semester[ \t]\d|full[ \t]?year)"
}

data_capture_regex = {
    # group 1 : student ID
    # group 2 : student name
    'student_id_name':
        re.compile(r"student id\s?:\s*(\d{8})\s*student name\s?:\s*([\w \-]*)", re.DOTALL | re.IGNORECASE),

    # group 1 : course ID
    # group 2 : course version
    'first_course_in_section':
        re.compile(
            r"course\s?:\s*^(\d{6}|[a-z]+-[a-z]+)\s*^v.\s?(\d)\s*attempt\s?:\s?\d[\s\S]*?(?=^\d{6}|^[a-z]+-[a-z]+)",
            re.MULTILINE | re.IGNORECASE),

    # courses that come after the first course line. matched as
    # [a collection of course IDs on multiple lines]
    # [a collection of corresponding versions on multiple lines]
    # group 1 : lines of courses
    # group 2 : lines of versions
    # todo : check if negative lookbehind is foolproof
    'next_courses':
        re.compile(r"((?:(?!^F-IN)(?<!^course:\n\n)^(?:[a-z]+-[a-z]+|[0-9]{6})$\s*)+)\s*((?:^v.\s?\d{1,2}$\s*)+)",
                   re.MULTILINE | re.IGNORECASE),

    # group 1 : reason for sanction
    'sanction':
        re.compile(r"^warning\s?:\s?this student has a current sanction.\s*reason\s?:\s*^([\s\S]*?(?=$))",
                   re.MULTILINE | re.IGNORECASE)

}

# regexes that are used to match all text upto a certain point. these are used by functions that deal with specific
# sections to progress the report to the point where the function is concerned with. (by stripping away everything
# before that)
#
# eg: when the function that processes the section with the list of courses is called, it removes everything upto the
# line "Course:"
match_everything_upto = {
    # eg : Course:
    'course':
        re.compile(r"[\s\S]*?(?=^course\s?:\s?$)", re.MULTILINE | re.IGNORECASE),

    # eg : Automatic Credit
    'automatic_or_recognition':
        re.compile(r"[\s\S]*?(?=^recognition of prior learning$|^automatic credit$)", re.MULTILINE | re.IGNORECASE),

    # eg : RECOGNITION OF PRIOR LEARNING
    'recognition_of_prior_learning':
        re.compile(r"[\s\S]+?(?=^recognition\sof\sprior\slearning$)", re.MULTILINE | re.IGNORECASE),

    # eg :  2015 Semester 2
    #       2016 full year
    #       Course:
    'next_semester':
        re.compile(r"[\s\S]+?(?=("
                   + raw_regexes['semester_sep']
                   + ")|^course\s?:$)", re.IGNORECASE | re.MULTILINE)
    # re.compile(r"[\s\S]+?(?=(^\d{4}[ \t]*(semester[ \t]\d|full[ \t]year))|^course\s?:$)", re.MULTILINE | re.I)
    # [\s\S]+?(?=^\d{4}[ \t]*(semester[ \t]\d|full[ \t]year)$)

}

data_groups = {
    # each regex in this dictionary captures a block of text containing (possibly multiple lines of) what is implied by
    # the key of the particular dictionary value.
    #
    # the regex uses negative lookahed to match all lines until it meets a line that is NOT what is being matched for
    # is found. this is to ensure that the search for the value being searched for is not cut short due to a rogue
    # empty newline inbetween valid values added by the pdfparser.
    # due to this the block of text can contain empty newlines in the middle that must be removed later.

    # unit id block
    'unit_id_group':
        re.compile(r"(?:^(\d{4,6}|[a-z]{4}\d{4})$\s*)+?(?!^(\d{4,6}|[a-z]{4}\d{4})$)", re.MULTILINE | re.IGNORECASE),

    # credits
    'credits_or_credit_received_group':
        re.compile(r"(?:^\d{1,2}\.\d{1,2}$\s*)+?(?!\d{1,2}\.\d{1,2})", re.MULTILINE | re.IGNORECASE),

    # unit versions
    'versions_group':
        re.compile(r"(?:^\d{1,2}$\s*)+?(?!\d{1,2})", re.MULTILINE | re.IGNORECASE),

    # unit statuses.
    # Note: IGNORECASE flag not set because all statuses are uppercase and there appears to be no
    # reason for them to be recorded in lowercase
    'unit_status_group':
        re.compile(r"(?:^(PASS|FAIL|ENR|PLN|WD)$\s*)+?(?!^(PASS|FAIL|ENR|PLN|WD)$)", re.MULTILINE)
}


def grab_next_unit_ids(rcv_text) -> (str, list):
    """
    grabs the first set of unit IDs that can be found on the arg 'text' and then removes it from the text
    ie. grabs :
    ----------
    COMP1000
    COMP2000

    ISAD3000
    ----------
    as a single block and then splits it to lines
    :param rcv_text: the report text from which the unit IDs are to be fetched
    :return str: the modified report text from which the matched block has been removed
    :return list: a list containing the (split) unit IDs fetched
    """
    # extracting data and modifying the report text
    regex = data_groups['unit_id_group']

    resultblock = regex.search(rcv_text).group(0)
    result_list = str(resultblock).splitlines(keepends=False)

    # removing empty entries
    result_list = [result for result in result_list if result is not ""]

    # removing everything upto, and including the extracted unitIDs from the source text (the report text)
    replace_upto_regex = re.compile(r"[\s\S]*?(?:^(\d{4,6}|[a-z]{4}\d{4})$\s*)+?(?!^(\d{4,6}|[a-z]{4}\d{4})$)",
                                    re.IGNORECASE | re.MULTILINE)
    rtr_text = strip_match(rcv_text, replace_upto_regex, repl_count=1)

    return rtr_text, result_list


def grab_next_credits(text) -> list:
    """
    grabs the first set of unit IDs that can be found on the arg 'text'.
    ie. grabs :
    ----------
    25.0

    25.0
    12.5
    ----------
    as a single block, splits it to lines and then removes empty entries (empty newlines)
    :param text: the report text from which the credits are to be fetched
    :return: a list containing the (split) credits fetched
    """
    credits_regex = data_groups['credits_or_credit_received_group']

    return fetch_group_and_splitlines(credits_regex, text)


def grab_next_versions(text) -> list:
    """
    grabs the first set of versions that can be found on the arg 'text'.
    ie. grabs :
    ----------
    1

    2
    4
    ----------
    as a single block, splits it to lines and then removes empty entries (empty newlines)
    :param text: the report text from which the versions are to be fetched
    :return: a list containing the (split) versions fetched
    """
    versions_regex = data_groups['versions_group']

    return fetch_group_and_splitlines(versions_regex, text)


def grab_next_unit_statuses(text) -> list:
    """
    grabs the first set of versions that can be found on the arg 'text'.
    ie. grabs :
    ----------
    PASS

    FAIL
    ENR
    PLN
    ----------
    as a single block, splits it to lines and then removes empty entries (empty newlines)
    :param text: the report text from which the unit statuses are to be fetched
    :return: a list containing the (split) statuses fetched
    """
    status_regex = data_groups['unit_status_group']

    return fetch_group_and_splitlines(status_regex, text)


def fetch_group_and_splitlines(regex, text) -> list:
    """
    internal function that offers functionality shared by multiple methods. fetches a block as specified by the regex
    and then return the non empty lines as a list.
    :param regex: the compiled regular expression object that is used to
    :param text: the report text from which the block is extracted from
    :return: a list containing the (split) results fetched
    """
    resultblock = regex.search(text).group(0)
    result_list = str(resultblock).splitlines(keepends=False)

    # removing empty entries
    result_list = [result for result in result_list if result is not ""]

    return result_list


def progress_upto(text, progup_regex) -> str:
    """
    progresses upto certain points of the report by removing all irrelevant/already parsed text before that point,
    leaving the parsed report data starting with the next section of relevant text so that the parser con continue from
    that point onwards. this function is in essence just a wrapper around the function strip_match() but exists for
    the sake of (hopefully) increasing readability of the code
    :param text: the parsed report text
    :param progup_regex: regular expression that specifies the location upto which the text should be trimmed to
                         (achieved through the use of lookaround assertions)
    :return: the parsed report text progressed upto the required point
    """
    return strip_match(text, progup_regex, repl_count=1)


def remove_garbage(text) -> str:
    """
    removes the garbage as specified in the dictionary 'garbage'
    :param text: the report text from which the 'garbage' values are to be removed
    :return: the tranformed report text
    """
    text = remove_spaces(text)
    for rgx_garbage_key in garbage.keys():
        if not rgx_garbage_key.startswith("skip"):
            text = garbage[rgx_garbage_key].sub("", text)
    # removing newlines or spaces at the start of report data
    text = re.sub(r"^\s*|\s*$", "", text)

    return text


def check_report_is_at_automatic_credit(text) -> bool:
    """
    checks if the current position of the report is the section titled "automatic credit". this check is performed since
    if the current section is indeed 'automatic credits', there exists an immediate "recognition of prior learning"
    section that follows. (which may or may not be empty)
    :param text: the report text to be checked
    :return: a boolean value that states whether the report is at said section
    """
    automatic_credit_check_regex = re.compile(r"^automatic\scredit", re.IGNORECASE).match(text)
    check_flag_auto = automatic_credit_check_regex is not None

    return check_flag_auto


def check_report_is_at_recognition_of_prior_learning(text) -> bool:
    """
    checks if the current position of the report is the section titled "recognition of prior learning".
    :param text: the report text to be checked
    :return: a boolean value that states whether the report is at said section
    """
    recog_check_regex = re.compile(r"^recognition\sof\sprior\slearning", re.IGNORECASE).match(text)
    check_flag_recog = recog_check_regex is not None

    return check_flag_recog


def check_recognition_of_prior_is_empty(text) -> bool:
    """
    checks if the "recognition of prior learning" section is empty. ie, whether it contains units for which credit is
    automatically awarded
    :param text: the report text
    :return: a boolean flag with the status of the condition in question
    """
    recog_empty_check_regex = \
        re.compile(r"^recognition\sof\sprior\slearning$\s*^planned\sand\scompleted\scomponents$",
                   re.IGNORECASE | re.MULTILINE).match(text)
    check_recog_empty_flag = recog_empty_check_regex is not None

    return check_recog_empty_flag


def check_current_semester_is_last_in_course(text) -> bool:
    """
    checks if the topmost semester on the report text is the last semester listed in the current course.
    ie. checks whether the current course has been parsed completely so that the parser can move on to the next
    course on the progress report if one exists
    :param text: the report text
    :return: a boolean flag that with the status of the condition in question
    """
    # regex matches a semester header line or a course line, which comes first is used to decide
    is_last_semester = re.compile(
        r"(^\d{4}[ \t]*(semester[ \t]\d|full[ \t]year)$)|(^course\s?:$)", re.MULTILINE | re.IGNORECASE)

    report_substring = text[text.index("\n") + 1:]
    result_match = is_last_semester.search(report_substring)

    if result_match is None:
        return True
    elif "course" in result_match.group(0).lower():
        return True
    else:
        return False


def check_course_section_exists(text) -> bool:
    """
    checks if a "course" section exists in the report text or not (ie. all course sections have been
    parsed and removed from the report text) if no more course sections exist, the parser has completed and can exist)
    :param text: the report text
    :return: a boolean flag that states the condition in question
    """
    check_rgx = re.compile(r"^course\s?:\s?$", re.IGNORECASE | re.MULTILINE)
    course_search = check_rgx.search(text)

    if course_search is None:
        return False
    return True


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
    :return: None. output is printed to stdout
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


def print_regex_groups(regex, remove_garbage_before=False):
    """
    function used to assist debugging regexes. returns groups matched by the regex passed on all pdf files in
    project dir
    :param regex: the compiled regular expression object to be checked
    :param remove_garbage_before:   flag that specifies whether garbage removal is to be performed on the report text
                                    before the regular expression is executed on it
    :return: None. output is printed to stdout
    """
    print("\n\nGroups for regex {} :".format(regex))

    for filepath in fetch_all_files():
        pdffile = PDFMinerWrapper(filepath).parse_data()
        pdftext = pdffile.text
        if remove_garbage_before is True:
            pdftext = remove_garbage(pdftext)

        regex_match_count = len(regex.findall(pdftext))
        print("\t{} matches in file [{}] : ".format(regex_match_count, pdffile.file_name))
        for index, regex_group in enumerate(regex.findall(pdftext)):
            print("\t\t{}:\t{}".format(index, regex_group))


def fetch_all_files():
    """
    fetches all pdf files located in project dir
    :return: a list containing the paths to pdf files
    """
    return glob.glob("*/**/*.pdf")
