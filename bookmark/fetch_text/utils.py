from io import StringIO
import random
import re
from typing import Tuple, Union, IO, List, Iterable

from lexrank import LexRank
from lexrank.mappings.stopwords import STOPWORDS

from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.pdfpage import PDFPage
from pdfminer.utils import open_filename

import spacy
from spacy.language import Language

import textacy
import textacy.ke



def extract_text(pdf_file: Union[IO, str], password: str = '', page_numbers: int = None, maxpages: int = 0,
                 caching : bool = True, codec : str = 'utf-8', laparams : LAParams = None) -> str:
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


def get_data_as_pages(data_dir: str, lang: Language, desc_size : int, desc_threshold : float) -> Tuple[str, int, str]:
    for path in data_dir:
        for pageno, page_text in extract_text(path):
            page_text = clean_text(page_text)
            yield path, pageno, page_text, get_keywords(page_text, lang), \
                  get_summary(break_into_sentences(page_text, lang), desc_size, desc_threshold)


def clean_text(page_text : str) -> str:
    page_text = re.sub('[^<\w.,\/\<\>?;:\'\"\[\]{}!@#$%\^&\*\-_+=`~()>]', ' ', page_text)
    page_text = re.sub('\s{2,}', ' ', page_text)
    return page_text


def get_keywords(data : str, lang : Language) -> List[str]:
    doc = textacy.make_spacy_doc(data, lang=lang)
    return list(map(lambda x: x[0], textacy.ke.scake(doc)))


def break_into_sentences(data : str, lang : Language) -> List[str]:
    doc = lang(data)
    return list(map(lambda sent: sent.text, doc.sents))


def get_summary(sentences : List[str], size : int, threshold : float) -> List[str]:
    try:
        return get_lex_summary(sentences, size, threshold)
    except:
        return get_random_summary(sentences, size)


def get_lex_summary(sentences : List[str], size : int, threshold : float) -> List[str]:
    lxr = LexRank(sentences, stopwords=STOPWORDS['en'])
    return lxr.get_summary(sentences, summary_size=size, threshold=threshold)


def get_random_summary(sentences : List[str], size : int) -> List[str]:
    return [sentences[i] for i in sorted(random.choices(range(len(sentences)), k=size))]