from pdfminer.pdfparser import PDFParser
from pdfminer.pdfdocument import PDFDocument
from pdfminer.pdfpage import PDFPage
from pdfminer.pdfpage import PDFTextExtractionNotAllowed
from pdfminer.pdfinterp import PDFResourceManager
from pdfminer.pdfinterp import PDFPageInterpreter
from pdfminer.pdfdevice import PDFDevice
from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams

from io import StringIO

import collections
import re


class PDFFile:
    def __init__(self, file_path, extracted_text, page_count):
        self.file_path = file_path

        self.pdf_extracted_text = extracted_text
        self.pdf_page_count = page_count

    def fetch_text(self):
        return self.pdf_extracted_text

    def fetch_page_count(self):
        return self.pdf_page_count


class PDFMinerWrapper:
    def __init__(self, file_path):
        self.file_path = file_path

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

        with open(self.file_path, "rb") as file:
            for page in PDFPage.get_pages(file, pagenos, maxpages=maxpages, password=password, caching=caching,
                                          check_extractable=True):
                self.pdf_page_count += 1
                interpreter.process_page(page)

        self.pdf_extracted_text = text_stream.getvalue()
        text_stream.close()
        device.close()

        return PDFFile(self.file_path, self.pdf_extracted_text, self.pdf_page_count)
