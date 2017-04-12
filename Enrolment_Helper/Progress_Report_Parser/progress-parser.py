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
multi_line = re.compile(r'\n{2,}')

# Regex for garbage found at the start of each progress report page
start_of_page_garbage_regex = re.compile(r'Curtin University[\s]+Student Progress Report[\s]+Student One[\s]+As At[\s]+')

# Regex for garbage found at the end of each progress report page
end_of_page_garbage_regex = re.compile(r'\[[0-9, a-z, A-Z]{5,}\](?s)(.*?)of[\s]+[0-9]+[\s]+')

# List of smaller, exact regex for garbage words and data
garbage_list = re.compile(r'(Student ID:|'  # Eliminates student ID label
                            'Student Name:|'  # Eliminates student name label
                            'Course:|'  # Eliminates course label
                            'Attempt:\s*[0-9]*|'  # Eliminates course attempts label and also the number
                            'Stage:\s*[A-Z]*|'  # Eliminates the stage label, and also the data
                            'Default Location: [A-Z, a-z]*|'  # Eliminates the location label, and also the data
                            'Not on plan|'  # Not on plans can be ignored

                            # Eliminates status, academic status labels and their data.
                            '(Academic\s*)?Status(:\s*(Good Standing|Conditional|Terminated|[A-Z]*)(\s*(Good Standing|Conditional|Terminated)?)?)?|'

                            # Eliminates labels for unit blocks
                            'BOE|'
                            'Final|'
                            'Grade|'
                            'Mark|'
                            'Credit[s]?|'
                            'On Study Plan\?|'
                            'Spk[A-Z, a-z]*|'  # All instances of Spk labels
                            'Ver|'
                            'SWA:\s*[0-9, .]*|'  # Plus data
                            'CWA:|'
                            'ADM|'
                            'POTC|'
                            '(Total\s*)?Automatic\s*Credit:?|'
                            'Received|'
                            'Total number of credits for course completion:|'
                            'Total number of credits completed:)\s+')



# # # # # # # # # # # # # # # # #
# MARKERS FOR REPLACING GARBAGE #
# # # # # # # # # # # # # # # # #

# Blank Replacement
blank_replacement = ''

# # # # # # # # # # # # # # # # #
#            METHODS            #
# # # # # # # # # # # # # # # # #

# Name:     remove_garbage
#
# Purpose:  Removes unneeded lines and data in the progress reporter output
#
# Params:   report: The progress report output (string)
#
# Return:   The improved proress report output (string)
#
# Notes:    None

def remove_garbage(report):

    # Replace start and end of page garbage with START OF PAGE and END OF PAGE
    report = re.sub(start_of_page_garbage_regex, blank_replacement, report)
    report = re.sub(end_of_page_garbage_regex, blank_replacement, report)

    # Remove other unneeded information and labels
    report = re.sub(garbage_list, blank_replacement, report)

    # Replace multiple newlines with one newline
    report = re.sub(multi_line, '\n', report)
    return report


    improved_report = report
    return improved_report


# Name:     convert_pdf_to_txt
#
# Purpose:  Extracts the text contents of a PDF into a string.
#
# Params:   path: The filepath of the PDF to be extracted from (string)
#
# Return:   The extracted text (string)
#
# Notes:    Works with pdfminer.six for Python 3.5.2 as of 11 April 2017

def convert_pdf_to_txt(path):
    rsrcmgr = PDFResourceManager()
    retstr = StringIO()
    codec = 'utf-8'
    laparams = LAParams()
    device = TextConverter(rsrcmgr, retstr, codec=codec, laparams=laparams)
    fp = open(path, 'rb')
    interpreter = PDFPageInterpreter(rsrcmgr, device)
    password = ""
    maxpages = 0
    caching = True
    pagenos=set()

    for page in PDFPage.get_pages(fp, pagenos, maxpages=maxpages, password=password,caching=caching, check_extractable=True):
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
    report = convert_pdf_to_txt(path)
    improved_report = remove_garbage(report)
    print(improved_report)

path = '/Users/CPedersen/Documents/SEP-2017/Progress-Report/Campbell-pr.pdf'
parse_progress_report(path)