import re

# dictionary containing required regular expressions
garbage = {
    # garbage at start of page
    # eg : Curtin University Student Progress Report Student One As At 21 Feb 2017
    "garbage_per_page_file_start":
        re.compile(r'curtin\s*university\s*student\s*progress\s*report\s*student\s*one\s*as\s*at\s*\d+\s*\w+\s*\d+\s*',
                   re.IGNORECASE),

    # garbage at the end of the page
    # eg : Page 1 of 3
    "garbage_per_page_page_number":
        re.compile(r"page\s*\d+\s*of\s*\d+\s*", re.IGNORECASE),

    # eg : Total number of credits for course completion: 1000.0
    "garbage_credits_for_course_completion":
        re.compile(r"total\s*number\s*of\s*credits\s*for\s*course\s*completion\s*:\s*\d+(\.\d+)?", re.IGNORECASE),

    # eg : Total number of credits completed: 325.0
    "garbage_credits_completed":
        re.compile(r"total\s*number\s*of\s*credits\s*completed\s*:\s*\d+(\.\d+)?", re.IGNORECASE),



}
