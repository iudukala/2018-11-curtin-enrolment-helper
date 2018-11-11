import regexes
from wrapper import PDFMinerWrapper


def main():
    for filepath in fetch_pdf_list():
        pdftext = PDFMinerWrapper(filepath).parse_data()
        pdftext = pdftext.text
        with open("initial output.txt", "w") as filehandle:
            filehandle.write(pdftext)

        for rgx_pat in regexes.garbage.values():
            regex_match_count = len(rgx_pat.findall(pdftext))
            pdftext = rgx_pat.sub("", pdftext)
            print("{} - {}".format(pdftext.count("\n"), filepath))

            # x = UnitInstance("COMP3002", "1", "25.0", "", "PASS")
            # x = Student("19329914", "isuru")
            # print(x)
        with open("final_output.txt", "w") as filehandle:
            filehandle.write(pdftext)

        for e in regexes.garbage.items():
            print(e[1])

def fetch_pdf_list():
    # return glob.glob("*/**/*.pdf")
    # return ['parser_tests/singlepage.pdf']
    return ["parser_tests/test_inputs/Campbell-pr.pdf"]


main()
