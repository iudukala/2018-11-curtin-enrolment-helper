import unittest
import glob

import regexes
from wrapper import PDFMinerWrapper


class RegexTestCases(unittest.TestCase):
    """tests if there exists a regex garbage match for each page"""
    def test_garbage_regex_per_page(self):
        for pdf_path in fetch_pdf_list():
            pdf_file = PDFMinerWrapper(pdf_path).parse_data()
            pdf_text = pdf_file.text
            pdf_pagecount = pdf_file.page_count

            for rgx_key in regexes.garbage.keys():
                if 'per_page' in rgx_key:
                    regex_match_count = len(regexes.garbage.get(rgx_key).findall(pdf_text))
                    self.assertTrue(pdf_pagecount == regex_match_count,
                                    msg="Failiure on per_page for [{}] on {}".format(rgx_key, pdf_path))


def fetch_pdf_list():
    return glob.glob("parser_tests/**/*.pdf")
    # return glob.glob("parser_tests/test_inputs/*.pdf")
    # return ["parser_tests/test_inputs/Campbell-pr.pdf"]


