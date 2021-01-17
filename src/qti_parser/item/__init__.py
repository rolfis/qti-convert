""" QTI Assessment Item """

from lxml import etree
from logzero import logger
import re
import hashlib
import config
from qti_parser import question_type

def get_question(xml_item):
    """ Get question, metadata and answers/options """
    xml_item_metadata = xml_item.find("{http://www.imsglobal.org/xsd/ims_qtiasiv1p2}itemmetadata/{http://www.imsglobal.org/xsd/ims_qtiasiv1p2}qtimetadata")
    this_question = {
        'id': str(xml_item.get("ident")),
        'title': str(xml_item.get("title")),
        'question_type': xml_item_metadata.find("{http://www.imsglobal.org/xsd/ims_qtiasiv1p2}qtimetadatafield[{http://www.imsglobal.org/xsd/ims_qtiasiv1p2}fieldlabel = 'question_type']/{http://www.imsglobal.org/xsd/ims_qtiasiv1p2}fieldentry").text,
        'points_possible': xml_item_metadata.find("{http://www.imsglobal.org/xsd/ims_qtiasiv1p2}qtimetadatafield[{http://www.imsglobal.org/xsd/ims_qtiasiv1p2}fieldlabel = 'points_possible']/{http://www.imsglobal.org/xsd/ims_qtiasiv1p2}fieldentry").text,
        'text': xml_item.find("{http://www.imsglobal.org/xsd/ims_qtiasiv1p2}presentation/{http://www.imsglobal.org/xsd/ims_qtiasiv1p2}material/{http://www.imsglobal.org/xsd/ims_qtiasiv1p2}mattext").text
    }

    image = []

    # Try and find images in text to separate them
    if this_question['text'].lower().find("<p>.*<img"):
        for match in re.finditer('<p>.*<img src=\"([^\"]+)\".*>.*</p>', this_question['text'], re.DOTALL):
            this_href = re.sub(r"\?.+$", "", match.group(1)).replace(config.img_href_ims_base, "")
            image.append({
                'id': str(hashlib.md5(this_href.encode()).hexdigest()),
                'href': this_href
            })
        p = re.compile('<p>.*<img src=\"([^\"]+)\".*>.*</p>')
        subn_tuple = p.subn('', this_question['text'])
        if subn_tuple[1] > 0:
            this_question['text'] = subn_tuple[0]

    elif this_question['text'].lower().find("<img"):
        for match in re.finditer('<img src=\"([^\"]+)\".*>', this_question['text'], re.DOTALL):
            this_href = re.sub(r"\?.+$", "", match.group(1)).replace(config.img_href_ims_base, "")
            image.append({
                'id': str(hashlib.md5(this_href.encode()).hexdigest()),
                'href': this_href
            })
        p = re.compile('<img src=\"([^\"]+)\".*>')
        subn_tuple = p.subn('', this_question['text'])
        if subn_tuple[1] > 0:
            this_question['text'] = subn_tuple[0]

    if image:
        this_question['image'] = image

    # Parse answers for each type of question
    if this_question['question_type'] == "multiple_choice_question":
        this_question['answer'] = question_type.multiple_choice.get_answers(xml_item)
    elif this_question['question_type'] == "true_false_question":
        this_question['answer'] = question_type.true_false.get_answers(xml_item)
    elif this_question['question_type'] == "multiple_answers_question":
        this_question['answer'] = question_type.multiple_answers.get_answers(xml_item)
    elif this_question['question_type'] == "short_answer_question":
        this_question['answer'] = question_type.short_answer.get_answers(xml_item)
    elif this_question['question_type'] == "fill_in_multiple_blanks_question":
        this_question['answer'] = question_type.fill_in_multiple_blanks.get_answers(xml_item)
    elif this_question['question_type'] == "multiple_dropdowns_question":
        this_question['answer'] = question_type.multiple_dropdowns.get_answers(xml_item)

    # Replace [variable] in question text with blanks
    if (this_question['question_type'] == "fill_in_multiple_blanks_question" or this_question['question_type'] == "multiple_dropdowns_question") and this_question['text'].find(r"\[(.*?)\]"):
        blank = config.blanks_replace_str * config.blanks_question_n
        p = re.compile(r"\[(.*?)\]")
        subn_tuple = p.subn(blank, this_question['text'])
        if subn_tuple[1] > 0:
            this_question['text'] = subn_tuple[0]
        if this_question['question_type'] == "multiple_dropdowns_question":
            this_question['text'] = question_type.multiple_dropdowns.enumerate_blanks(this_question['text'])

    return this_question
