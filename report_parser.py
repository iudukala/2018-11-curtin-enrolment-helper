import glob
import pprint
import re
from wrapper import PDFMinerWrapper, PDFFile
import regexes


def main():
    # campdf = PDFMinerWrapper("parser_tests/test_inputs/Campbell-pr.pdf")
    # camtext = campdf.extract_text()
    # campages = campdf.

    # pdflist = glob.glob("*/**/*.pdf")
    # pprint.PrettyPrinter(4).pprint(pdflist)

    # pat = re.compile(regexes.garbage_file_start, re.IGNORECASE)

    # print(pdf_text)
    # print(pat.findall(pdf_text))
        # pprint.PrettyPrinter(3).pprint(pat.findall(text))
        # print(len(pat.findall(text)) == pdfobj.get_page_count())

    # print(regexes.garbage.values())

    for regex_str in regexes.garbage.values():
        pattern = re.compile(regex_str, re.IGNORECASE)

        for filepath in fetch_pdf_list():
            pdffile = PDFMinerWrapper(filepath).parse_data()
            pdftext = pdffile.fetch_text()

            print("{} - {}".format(pdftext.count("\n"), filepath))
            pdftext = pattern.sub("", pdftext)
            print(pdftext)


def fetch_pdf_list():
    # return glob.glob("*/**/*.pdf")
    return ['parser_tests/singlepage.pdf']


main()
