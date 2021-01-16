"""
Multiple Dropdowns
Select one answer for each blank from a list of answers
"""

from lxml import etree
from logzero import logger
import re
import hashlib
import config

def get_answers(xml):
    """ Return an array of possible answers, grouped for each blank """
    answers_group = []
    correct_answer = {}

    for id in xml.findall(".//{http://www.imsglobal.org/xsd/ims_qtiasiv1p2}varequal"):
        correct_answer[id.get("respident")] = id.text

    try:
        for xml_response_lid in xml.findall(".//{http://www.imsglobal.org/xsd/ims_qtiasiv1p2}response_lid"):
            answers = []

            for xml_answer_item in xml_response_lid.findall(".//{http://www.imsglobal.org/xsd/ims_qtiasiv1p2}response_label"):
                this_answer = {}
                this_answer['id'] = xml_answer_item.get("ident")
                this_answer['text'] = xml_answer_item.find("{http://www.imsglobal.org/xsd/ims_qtiasiv1p2}material/{http://www.imsglobal.org/xsd/ims_qtiasiv1p2}mattext").text
                this_answer['correct'] = True if xml_response_lid.get("ident") in correct_answer and correct_answer[xml_response_lid.get("ident")] == this_answer['id'] else False
                this_answer['display'] = True
                answers.append(this_answer)

            answers_group.append({
                'group_id': xml_response_lid.get("ident"),
                'options': answers
            })

    except OSError as e:
        logger.error("%s", e)
    except etree.ParseError as e:
        logger.error("XML parser error: %s", e)
    return answers_group