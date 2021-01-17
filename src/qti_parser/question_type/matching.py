"""
Matching Question
Select one matching answer for each item in a list
"""

from lxml import etree
from logzero import logger
from random import shuffle
import re
import hashlib
import config

def get_answers(xml):
    """ Return an array of items and possible answers """
    answers = []
    correct_answer = {}

    for id in xml.findall(".//{http://www.imsglobal.org/xsd/ims_qtiasiv1p2}varequal"):
        correct_answer[id.get("respident")] = id.text

    try:
        for xml_response_lid in xml.findall(".//{http://www.imsglobal.org/xsd/ims_qtiasiv1p2}response_lid"):
            this_response_lid = {
                'id': xml_response_lid.get("ident"),
                'text': xml_response_lid.find("./{http://www.imsglobal.org/xsd/ims_qtiasiv1p2}material/{http://www.imsglobal.org/xsd/ims_qtiasiv1p2}mattext").text,
                'display': True,
                'options': []
            }

            for xml_option in xml_response_lid.findall(".//{http://www.imsglobal.org/xsd/ims_qtiasiv1p2}response_label"):
                this_option = {}
                this_option['id'] = xml_option.get("ident")
                this_option['text'] = xml_option.find("{http://www.imsglobal.org/xsd/ims_qtiasiv1p2}material/{http://www.imsglobal.org/xsd/ims_qtiasiv1p2}mattext").text
                this_option['display'] = True
                this_option['correct'] = True if this_response_lid['id'] in correct_answer and correct_answer[this_response_lid['id']] == xml_option.get("ident") else False
                this_response_lid['options'].append(this_option)

            if config.matching_random_shuffle_answer_options:
                shuffle(this_response_lid['options'])
                
            answers.append(this_response_lid)

    except OSError as e:
        logger.error("%s", e)
    except etree.ParseError as e:
        logger.error("XML parser error: %s", e)

    if config.matching_random_shuffle_answers:
        shuffle(answers)

    return answers
