"""
Microsoft Word 2007 Format
"""

from docx import Document
from docx.shared import Mm
from docx.enum.text import WD_BREAK
from htmldocx import HtmlToDocx
from logzero import logger

def write_file(data):
    doc = Document()
    doc = setup_a4(doc)
    doc = setup_metadata(doc)

    html_parser = HtmlToDocx()

    for assessment in data['assessment']:
        doc.add_heading(assessment['title'], 0)
        for question in assessment['question']:
            if 'image' in question:
                for img in question['image']:
                    doc.add_picture(img['href'].replace("%20", " "), width=Mm(100))
            if 'text' in question:
                html_parser.add_html_to_document(question['text'], doc)
            if 'answer' in question:                
                for index, answer in enumerate(question['answer']):
                    if answer['display']:
                        if 'image' in answer:
                            for img in answer['image']:
                                html_parser.add_html_to_document("<p>" + str(index+1) + ".</p>", doc)
                                doc.add_picture(img['href'].replace("%20", " "), height=Mm(10))
                        if 'text' in answer and answer['text'] != '':
                            html_parser.add_html_to_document("<p>" + str(index+1) + ". </p>" + answer['text'], doc)
                    else:
                        doc.add_paragraph("_" * 80)

            doc.add_page_break()

    doc.save("output.docx")

def setup_a4(document):
    section = document.sections[0]
    section.page_height = Mm(297)
    section.page_width = Mm(210)
    section.left_margin = Mm(20)
    section.right_margin = Mm(30)
    section.top_margin = Mm(20)
    section.bottom_margin = Mm(20)
    section.header_distance = Mm(12)
    section.footer_distance = Mm(12)
    return document

def setup_metadata(document):
    properties = document.core_properties
    properties.author = "qti-converter"
    properties.title = "Quiz export from LMS"
    return document
