# Author    : Isuru Udukala (iudukala@gmail.com)


from io import StringIO

from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams
from pdfminer.pdfinterp import PDFPageInterpreter
from pdfminer.pdfinterp import PDFResourceManager
from pdfminer.pdfpage import PDFPage


class PDFFile:
    def __init__(self, file_name, extracted_text, page_count):
        self.file_name = file_name

        self.text = extracted_text
        self.page_count = page_count


class PDFMinerWrapper:
    def __init__(self, fp):
        self.fp = fp

        self.file_name = None
        self.pdf_processed = False
        self.pdf_extracted_text = None
        self.pdf_page_count = -1

    def parse_data(self):
        rsrcmgr = PDFResourceManager()
        text_stream = StringIO()
        codec = 'utf-8'
        laparams = LAParams()
        laparams.boxes_flow = 0.5
        device = TextConverter(rsrcmgr, text_stream, codec=codec, laparams=laparams)
        interpreter = PDFPageInterpreter(rsrcmgr, device)
        password = ""
        maxpages = 0
        caching = True
        pagenos = set()

        self.pdf_page_count = 0

        for page in PDFPage.get_pages(self.fp, pagenos, maxpages=maxpages, password=password, caching=caching,
                                      check_extractable=True):
            self.pdf_page_count += 1
            interpreter.process_page(page)

        self.file_name = self.fp.name
        self.fp.close()
        self.pdf_extracted_text = text_stream.getvalue()
        text_stream.close()
        device.close()

        return PDFFile(self.file_name, self.pdf_extracted_text, self.pdf_page_count)
