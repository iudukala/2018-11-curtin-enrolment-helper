from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams
from pdfminer.pdfpage import PDFPage
from io import StringIO
import re

# # # # # # # # # # # # # # # # #
# REGULAR EXPRESSIONS (compiled)#
# # # # # # # # # # # # # # # # #

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
remove_all_unneeded_strings = re.compile(r'^(?!Course:|Elective|[0-9]{4}|\bNot assigned\b).+[a-z]+.*$', re.MULTILINE)

# List of smaller, exact regex for garbage words and data
garbage_list = re.compile(r'(BOE|'
                            'Final|'
                            'Grade|'
                            'Mark|'
                            'Spk[A-Z, a-z]*|'  # All instances of Spk labels
                            'Ver|'
                            'SWA:\s*[0-9, .]*|'  # Plus data
                            'CWA:|'
                            'ADM|'
                            'POTC|'
                            'Type|'
                            'Student ID:|'
                            'Student Name:|'
                            'Total number of credits for course completion: [0-9, .]+|'
                            'Total number of credits completed: [0-9, .]+|'
                            'Total Recognition of Prior Learning(.*?)[0-9, .]+|'
                            'PLANNED AND COMPLETED COMPONENTS|'
                            'RECOGNITION OF PRIOR LEARNING)', re.MULTILINE)

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
# Params:   report: The progress report output (string)
#
# Return:   A dictionary, containing the report date, students name, and ID, and the report
#           with these details removed.
#
# Notes:    None
def extract_student_details(report):
    dict = {}
    splitLines = report.split('\n')
    dict['date'] = splitLines[1]
    dict['id'] = splitLines[3]
    dict['name'] = splitLines[4]
    report = re.sub(remove_start_of_page_regex, '', report)
    report = re.sub(remove_all_unneeded_strings, '', report)
    report = re.sub(multiple_newline, '\n', report)
    return dict, report

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
# Params:   path: The filepath of the PDF to be extracted from (string)
#
# Return:   A JSON-structured python dictionary representing the student's progress report.
#
# Notes:    Only importing this method is necessary.

def parse_progress_report(path):
    report = convert_pdf_to_txt(path) # Converts PDF to text
    report = remove_garbage(report) # Removes unneeded labels from report
    report_dict, report = extract_student_details(report) # Extracts student details, including report date
    print(report)
    print(report_dict)

paths = ['/Users/CPedersen/Documents/SEP-2017/Progress-Report/Darryl-pr.pdf']#,
         # '/Users/CPedersen/Documents/SEP-2017/Progress-Report/ChienFeiLin-pr.pdf',
         # '/Users/CPedersen/Documents/SEP-2017/Progress-Report/Darryl-pr.pdf',
         # '/Users/CPedersen/Documents/SEP-2017/Progress-Report/Derrick-pr.pdf',
         # '/Users/CPedersen/Documents/SEP-2017/Progress-Report/Eugene-pr.pdf',
         # '/Users/CPedersen/Documents/SEP-2017/Progress-Report/Steven-pr.pdf',
         # '/Users/CPedersen/Documents/SEP-2017/Progress-Report/XiMingWong-First-pr.pdf',
         # '/Users/CPedersen/Documents/SEP-2017/Progress-Report/XiMingWong-Second-pr.pdf',
         # '/Users/CPedersen/Documents/SEP-2017/Progress-Report/Yoakim-pr.pdf']
for path in paths:
    fp = open(path, 'rb')
    parse_progress_report(fp)