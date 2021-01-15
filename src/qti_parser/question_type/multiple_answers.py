"""
Multiple Answers
"""

from lxml import etree
from logzero import logger

def get_answers(xml):
    """ Return an array of possible answers """
    answers = []
    correct_answers = []

    for id in xml.findall(".//{http://www.imsglobal.org/xsd/ims_qtiasiv1p2}conditionvar/{http://www.imsglobal.org/xsd/ims_qtiasiv1p2}and/{http://www.imsglobal.org/xsd/ims_qtiasiv1p2}varequal"):
        correct_answers.append(id.text)

    try:
        for xml_answer_item in xml.findall(".//{http://www.imsglobal.org/xsd/ims_qtiasiv1p2}response_label"):
            answers.append(
                {
                    'id': xml_answer_item.get("ident"),
                    'text': xml_answer_item.find("{http://www.imsglobal.org/xsd/ims_qtiasiv1p2}material/{http://www.imsglobal.org/xsd/ims_qtiasiv1p2}mattext").text,
                    'correct': True if xml_answer_item.get("ident") in correct_answers else False,
                    'display': True
                }
            )
    except OSError as e:
        logger.error("%s", e)
    except etree.ParseError as e:
        logger.error("XML parser error: %s", e)
    return answers