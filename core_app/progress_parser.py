from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams
from pdfminer.pdfpage import PDFPage
from io import StringIO
import re

# # # # # # # # # # # # # # # # #
# REGULAR EXPRESSIONS (compiled)#
# # # # # # # # # # # # # # # # #

# Regex for finding specific data points in the report output
course_id_regex = re.compile(r'^([0-9, A-Z]+-)?[0-9, A-Z]{4,}$')

semester_header_regex = re.compile(r'^([0-9]{4}\s+Semester\s+[1-2]{1}|Automatic Credit|Exempt|Not Assigned.*)$')
unit_id_regex = re.compile(r'(^[A-Z]{4}[0-9]{4}$|^[0-9]{4,})$')
version_regex = re.compile(r'^[0-9]{1,2}$')
credit_value_regex = re.compile(r'^[0-9]{1,3}\.[0-9]{1,2}$')
unit_status_regex = re.compile(r'^(PASS|FAIL|PLN|ENR|WD)$')

# Regex for eliminating multiple lines
multiple_newline = re.compile(r'\n{2,}')
start_of_line_spaces = re.compile(r'^ +', re.MULTILINE)
end_of_line_spaces = re.compile(r' +$', re.MULTILINE)

# Regex for garbage found at the start of each progress report page
start_of_page_garbage_regex = re.compile(r'Curtin University[\s]+Student Progress Report[\s]+Student One[\s]+As At[\s]+')

# Regex for garbage found at the end of each progress report page
page_number_garbage_regex = re.compile(r'(Page\s*[0-9]+(\s)+of[\s]+[0-9]+[\s]+)')
report_id_garbage_regex = re.compile(r'(\[[0-9, a-z, A-Z]{10}\]|[0-9]{6}[A-Z]{1})')
report_timestamp_garbage_regex = re.compile(r'[0-9]{1,2}:[0-9]{1,2}:[0-9]{1,2}(AM|PM)')
remove_start_of_page_regex = re.compile(r'(START OF PAGE)\s+(.*\s){3}')
remove_all_unneeded_strings_regex = re.compile(r'^(?!Course:|Automatic|Exempt|Elective|[0-9]{4}|\bNot assigned\b|\bElective not yet selected\b).+[a-z]+.*$', re.MULTILINE)
remove_exempt_regex = re.compile(r'Exempt\s*')

# List of smaller, exact regex for garbage words and data
garbage_list = re.compile(r'(^BOE$|'
                            '^Final$|'
                            '^Grade$|'
                            '^Mark$|'
                            '^SWA:\s*[0-9, .]*$|'  # Plus data
                            '^CWA:.*|'
                            '^ADM$|'
                            '^POTC$|'
                            '^Type$|'
                            '^Student ID:$|'
                            '^Student Name:$|'
                            '^Total number of credits for course completion: [0-9, .]+$|'
                            '^Total number of credits completed: [0-9, .]+$|'
                            '^Total Recognition of Prior Learning(.*?)[0-9, .]+$|'
                            '^PLANNED AND COMPLETED COMPONENTS$|'
                            '^RECOGNITION OF PRIOR LEARNING$|'
                            '^v. |'
                            '^Student Name: )', re.MULTILINE)

# # # # # # # # # # # # # # # # #
#            METHODS            #
# # # # # # # # # # # # # # # # #

# Name:     remove_garbage
#
# Purpose:  Removes unneeded lines and data in the progress reporter output
#
# Params:   report: The progress report output (string)
#
# Return:   The improved progress report output (string)
#
# Notes:    None
def remove_garbage(report):
    # Replace start and end of page garbage. Start of page signified by 'START OF PAGE'
    report = re.sub(start_of_page_garbage_regex, 'START OF PAGE\n', report)
    report = re.sub(report_id_garbage_regex, '', report)
    report = re.sub(page_number_garbage_regex, '', report)
    report = re.sub(report_timestamp_garbage_regex, '', report)

    # Remove other unneeded information and labels
    report = re.sub(garbage_list, '', report)

    # Remove all gross unneeded whitespace
    report = re.sub(multiple_newline, '\n', report)
    report = re.sub(start_of_line_spaces, '', report)
    report = re.sub(end_of_line_spaces, '', report)

    return report


# Name:     extract_student_details
#
# Purpose:  Extracts the report date, student ID and student name. Also further unlabels input.
#
# Params:   report: The progress report output after being thrown into remove_garbage (string)
#
# Return:   A dictionary, containing the report date, students name, and ID, and the report
#           with these details removed. Also, the newly neutered report string.
#
# Notes:    None
def extract_student_details(report):
    dict = {}
    splitLines = report.split('\n')
    dict['date'] = splitLines[1]
    dict['id'] = splitLines[3]
    dict['name'] = splitLines[4]
    report = re.sub(remove_start_of_page_regex, '', report)
    report = re.sub(remove_all_unneeded_strings_regex, '', report)
    if 'Exempt' in report and 'Automatic' in report:
        report = re.sub(remove_exempt_regex, '', report)
    report = re.sub(multiple_newline, '\n', report)
    return dict, report


# Name:     extract_progress_details
#
# Purpose:  Extracts the student's most recent course, and the units a student has completed
#           (both in that course and outside that course, to count unit attempts in the backend)
#
# Params:   report: The progress report output after being thrown into extract_student_details (string)
#           report_dict: A python dictionary containing a student's details.
#
# Return:   A python dictionary which now contains a student's progress details.
#
# Notes:    None
def extract_progress_details(report, report_dict):
    lines = report.split('\n')  # Split report into lines
    indexCount = len(lines) - 1
    i = 0  # Index for line counting
    ignoredUnits = set()  # Variable stores unit IDs the parser should ignore in future
    ignoredVersions = set()  # Variable stores unit versions the parser should ignore in future
    ignoredCredits = set()  # Variable stores unit credit worths the parser should ignore in future
    ignoredStatus = set()  # # Variable stores unit statuses the parser should ignore in future
    units = {}  # Variable stores all units in a dictionary
    unitsAuto = {}  # Varible stores the most recently automatically credited units list


    while not lines[i]:  # Go to start of file, skipping any whitespace (if applicable)
        i += 1

    while i < indexCount:  # While not at end of file (Essentially, for each course)

        # Go to next instance of course from start of file
        while i < indexCount and 'Course' not in lines[i]:
            i += 1

        # Replace current course detail with new detail
        report_dict, i = extract_course_details(lines, report_dict, i)

        # Clear credited units for previous courses
        unitsAuto = {}

        # Now you're at first semester header
        semHeaderRecent = lines[i]
        semHeaderRecentIdx = i

        # For each semester header, extract information about units completed.
        while i < indexCount and 'Course' not in lines[i]:  # While not at EOF and not at the next course header
            semHeaderPrev = semHeaderRecent  # Keep track of last sem header seen
            while i < indexCount and ('Course' not in lines[i] and semHeaderRecent == semHeaderPrev):  # For each semester
                semUnitIDs = []  # Stores the units taken in each semester
                semUnitDetails = []  # Stores the units version, credit worth and status as dictionaries

                i = semHeaderRecentIdx  # Go to last known semester header and try again

                ### GET UNIT IDs ###
                # Advance to first unit ID from semester header that hasn't been read already
                while (i < indexCount and not re.match(unit_id_regex, lines[i])) or i in ignoredUnits:
                    i, semHeaderRecent, semHeaderRecentIdx = advance_line(lines, i, semHeaderRecent, semHeaderRecentIdx)

                while re.match(unit_id_regex, lines[i]):  # Iterate unit ID list
                    semUnitIDs.append(lines[i])  # Add unit ID to list
                    ignoredUnits.add(i)  # Add current line to ignored index list
                    i, semHeaderRecent, semHeaderRecentIdx = advance_line(lines, i, semHeaderRecent, semHeaderRecentIdx)

                ### GET UNIT VERSIONS ###
                # Advance to first version from semester header that hasn't been read already
                while (i < indexCount and not re.match(version_regex, lines[i])) or i in ignoredVersions:
                    i, semHeaderRecent, semHeaderRecentIdx = advance_line(lines, i, semHeaderRecent, semHeaderRecentIdx)

                for count in range(0, len(semUnitIDs)):  # Iterate version list
                    semUnitDetails.append({'ver': lines[i]})  # Add unit version to list
                    ignoredVersions.add(i)  # Add current line to ignored version list
                    i, semHeaderRecent, semHeaderRecentIdx = advance_line(lines, i, semHeaderRecent, semHeaderRecentIdx)

                ### GET UNIT CREDIT WORTH ###
                # Advance to first credit worth from semester header that hasn't been read already
                while (i < indexCount and not re.match(credit_value_regex, lines[i])) or i in ignoredCredits:
                    i, semHeaderRecent, semHeaderRecentIdx = advance_line(lines, i, semHeaderRecent, semHeaderRecentIdx)

                for count in range(0, len(semUnitIDs)):  # Iterate credit worth list
                    semUnitDetails[count].update({'credits': lines[i]})  # Add credit worth to list
                    ignoredCredits.add(i)  # Add current line to ignored version list
                    i, semHeaderRecent, semHeaderRecentIdx = advance_line(lines, i, semHeaderRecent, semHeaderRecentIdx)

                # If in automatic credit or exempt semester, add last credit num (total credits) to ignore list

                ### GET UNIT STATUS ###
                if 'Automatic' in semHeaderPrev or 'Exempt' in semHeaderPrev:  # If in autocredit header
                    ignoredCredits.add(i)  # Add total credit value to ignore list, then advance beyond that.
                    i, semHeaderRecent, semHeaderRecentIdx = advance_line(lines, i, semHeaderRecent, semHeaderRecentIdx)
                    # If no credit information is between this line and next header, advance to next header
                    if no_remaining_units(i, lines, ignoredCredits):
                        while i < indexCount and not re.match(semester_header_regex, lines[i]):
                            i, semHeaderRecent, semHeaderRecentIdx = advance_line(lines, i, semHeaderRecent, semHeaderRecentIdx)
                else:  # If in actual semester
                    # Advance to first unit status from semester header that hasn't been read already
                    while (i < indexCount and not re.match(unit_status_regex, lines[i])) or i in ignoredStatus:
                        i, semHeaderRecent, semHeaderRecentIdx = advance_line(lines, i, semHeaderRecent, semHeaderRecentIdx)

                    for count in range(0, len(semUnitIDs)):  # Iterate unit status list
                        semUnitDetails[count].update({'status': lines[i]})  # Add unit status to list
                        ignoredStatus.add(i)  # Add current line to ignored version list
                        i, semHeaderRecent, semHeaderRecentIdx = advance_line(lines, i, semHeaderRecent, semHeaderRecentIdx)

                ### ADD UNITS TO DICTIONARY ###
                for index, unit in enumerate(semUnitIDs):
                    if 'Automatic' in semHeaderPrev or 'Exempt' in semHeaderPrev:
                        unitsAuto.update({unit: semUnitDetails[index]})
                    else:
                        extender = 1
                        while(unit in units):
                            extender += 1
                            unit = unit + '~:' + str(extender)
                        units.update({unit: semUnitDetails[index]})
    report_dict['units'] = units
    report_dict['automatic'] = unitsAuto
    return report_dict

# Name:     no_remaining_units
#
# Purpose:  Checks if all unit IDs in the automatic semester header have been covered fully
#
# Params:   i: Current line number the parser is reading
#           lines: The progress report output after being thrown into extract_student_details (list of lines).
#           ignoredCredits: A set containing already read credit values
#
# Return:   False if there are units remaining, true if there are no units remaining
#
# Notes:    Should only be called from extract_progress_details
def no_remaining_units(i, lines, ignoredCredits):
    noneRemaining = True
    nextSemHeader = i

    # Go to next header and store its line index
    while not re.match(semester_header_regex, lines[nextSemHeader]):
        nextSemHeader += 1

    # If between current position and header there is a credit value, return true instead of false.
    for count in range(i, nextSemHeader):
        if re.match(credit_value_regex, lines[count]) and lines[count] not in ignoredCredits:
            noneRemaining = False
    return noneRemaining

# Name:     advance_line
#
# Purpose:  Advances the line number in the parser, while checking for a new semester header
#
# Params:   lines: The progress report output after being thrown into extract_student_details (list of lines).
#           i: The current line number the parser is reading
#           semHeaderRecent: The last unique semester header that the parser has hit
#           semHeaderPrevIdx: The line index of the last unique semester header that the parser has hit
#
# Return:   i, the newly incremented line counter and semHeaderPrev, the updated (or not) semester header
#
# Notes:    Should only be called from extract_progress_details
def advance_line(lines, i, semHeaderRecent, semHeaderRecentIdx):
    i += 1
    if re.match(semester_header_regex, lines[i]):
        semHeaderRecent = lines[i]
        semHeaderRecentIdx = i
    return i, semHeaderRecent, semHeaderRecentIdx


# Name:     extract_course_details
#
# Purpose:  Extracts the current course that the line index of the parser is at.
#
# Params:   lines: The progress report output after being thrown into extract_student_details (list of lines)
#           report_dict: A python dictionary containing a student's details.
#           i: The current position of the parser's 'cursor'.
#
# Return:   A python dictionary which now contains course details, and the index the parser is at.
#
# Notes:    None
def extract_course_details(lines, report_dict, i):
    courseDetails = {}
    ignoredVersions = set()
    semHeader = True
    while i < len(lines) - 1 and semHeader:  # Loop through and extract course details
        if re.match(course_id_regex, lines[i]):  # When a course ID is hit
            course = lines[i]  # Store it and go fetch the version
            courseIndex = i  # Store line index of course ID to return to later
            while not re.match(version_regex, lines[i]) or i in ignoredVersions:  # When an unread version is hit
                i += 1
            ignoredVersions.add(i)
            version = lines[i]  # Store version
            i = courseIndex + 1  # Return to the line after the course ID
            courseDetails[course] = version
        elif re.match(semester_header_regex, lines[i]):
            semHeader = False
        else:
            i += 1
    report_dict['course'] = courseDetails
    return report_dict, i


# Name:     convert_pdf_to_txt
#
# Purpose:  Extracts the text contents of a PDF into a string.
#
# Params:   path: The file pointer of the PDF to be extracted from (string)
#
# Return:   The extracted text (string)
#
# Notes:    Works with pdfminer.six for Python 3.5.2 as of 11 April 2017
def convert_pdf_to_txt(fp):
    rsrcmgr = PDFResourceManager()
    retstr = StringIO()
    codec = 'utf-8'
    laparams = LAParams()
    laparams.boxes_flow = 0.5
    device = TextConverter(rsrcmgr, retstr, codec=codec, laparams=laparams)
    interpreter = PDFPageInterpreter(rsrcmgr, device)
    password = ""
    maxpages = 0
    caching = True
    pagenos=set()

    for page in PDFPage.get_pages(fp, pagenos, maxpages=maxpages, password=password, caching=caching, check_extractable=True):
        interpreter.process_page(page)

    text = retstr.getvalue()

    fp.close()
    device.close()
    retstr.close()
    return text


# Name:     parse_progress_report
#
# Purpose:  Extracts PDF contents and interprets the results into a JSON-structured python dictionary.
#
# Params:   fp: The file pointer of the pdf file to parse
#
# Return:   A JSON-structured python dictionary representing the student's progress report.
#
# Notes:    IMPORT THIS METHOD, THEN CALL IT
def parse_progress_report(fp):
    report = convert_pdf_to_txt(fp) # Converts PDF to text
    report = remove_garbage(report) # Removes unneeded labels from report
    report_dict, report = extract_student_details(report) # Extracts student details, including report date
    report_dict = extract_progress_details(report, report_dict)  # Extracts unit details, including units done and units planned
    return report_dict

# Test code
paths = ['/home/yoakim/2017/SEP2/SEP2_Project/PDF_PLANS/StudentProgressReport-17080170-27_Mar_2017.pdf'#, 
        # '/Users/CPedersen/Documents/SEP-2017/Progress-Report/Campbell-pr.pdf']#,
        # '/Users/CPedersen/Documents/SEP-2017/Progress-Report/Campbell.pdf', < Works
         # '/Users/CPedersen/Documents/SEP-2017/Progress-Report/ChienFeiLin-pr.pdf',
         # '/Users/CPedersen/Documents/SEP-2017/Progress-Report/Darryl-pr.pdf',
         # '/Users/CPedersen/Documents/SEP-2017/Progress-Report/Derrick-pr.pdf',
         # '/Users/CPedersen/Documents/SEP-2017/Progress-Report/Eugene-pr.pdf',
         # '/Users/CPedersen/Documents/SEP-2017/Progress-Report/Steven-pr.pdf',
         # '/Users/CPedersen/Documents/SEP-2017/Progress-Report/XiMingWong-First-pr.pdf',
         # '/Users/CPedersen/Documents/SEP-2017/Progress-Report/XiMingWong-Second-pr.pdf', < Works
         # '/Users/CPedersen/Documents/SEP-2017/Progress-Report/Yoakim-pr.pdf']
         ]
for path in paths:
    fp = open(path, 'rb')
    parse_progress_report(fp)
