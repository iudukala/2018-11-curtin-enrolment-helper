# Author    : Isuru Udukala (iudukala@gmail.com)


import glob
import unittest

from core_app.parser import regex_handler
from core_app.parser.wrapper import PDFMinerWrapper


class RegexTestCases(unittest.TestCase):
    """tests if there exists a regex garbage match for each page"""

    def test_garbage_regex_per_page(self):
        for pdf_path in fetch_pdf_list():
            pdf_file = PDFMinerWrapper(pdf_path).parse_data()
            pdf_text = pdf_file.text
            pdf_pagecount = pdf_file.page_count

            for rgx_key in regex_handler.garbage.keys():
                if 'per_page' in rgx_key:
                    regex_match_count = len(regex_handler.garbage.get(rgx_key).findall(pdf_text))
                    self.assertTrue(pdf_pagecount == regex_match_count,
                                    msg="Failiure on per_page for [{}] on {}".format(rgx_key, pdf_path))


def fetch_pdf_list():
    return glob.glob("parser_tests/**/*.pdf")


if __name__ == '__main__':
    unittest.main()
