from io import StringIO
import re
from typing import Tuple

from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.pdfpage import PDFPage
from pdfminer.utils import open_filename

import spacy


def extract_text(pdf_file, password='', page_numbers=None, maxpages=0,
                 caching=True, codec='utf-8', laparams=None):
    """Parse and return the text contained in a PDF file.

    :param pdf_file: Either a file path or a file-like object for the PDF file
        to be worked on.
    :param password: For encrypted PDFs, the password to decrypt.
    :param page_numbers: List of zero-indexed page numbers to extract.
    :param maxpages: The maximum number of pages to parse
    :param caching: If resources should be cached
    :param codec: Text decoding codec
    :param laparams: An LAParams object from pdfminer.layout. If None, uses
        some default settings that often work well.
    :return: a string containing all of the text extracted.
    """
    if laparams is None:
        laparams = LAParams()

    with open_filename(pdf_file, "rb") as fp, StringIO() as output_string:
        rsrcmgr = PDFResourceManager()
        device = TextConverter(rsrcmgr, output_string, codec=codec,
                               laparams=laparams)
        interpreter = PDFPageInterpreter(rsrcmgr, device)

        for pageno, page in enumerate(PDFPage.get_pages(
                fp,
                page_numbers,
                maxpages=maxpages,
                password=password,
                caching=caching,
                check_extractable=True,
        )):
            output_string.seek(0)
            output_string.truncate(0)
            interpreter.process_page(page)

            yield pageno, output_string.getvalue()


def get_data_as_pages(data_dir) -> Tuple[str, int, str]:
    for path in data_dir:
        for pageno, page_text in extract_text(path):
            page_text = re.sub('[^<\w.,\/\<\>?;:\'\"\[\]{}!@#$%\^&\*\-_+=`~()>]', ' ', page_text)
            page_text = re.sub('\s{2,}', ' ', page_text)
            yield path, pageno, page_text


def get_data_as_sentences() -> Tuple[str, int, str]:
    nlp = spacy.load("en_core_web_sm")
    for path, pageno, page_text in get_data_as_pages():
        doc = nlp(page_text)
        for sent in doc.sents:
            yield path, pageno, sent.text


def get_keywords():
    pass