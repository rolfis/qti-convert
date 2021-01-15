"""
Short Answer
"""

from lxml import etree
from logzero import logger

def get_answers(xml):
    """ Return an array of possible answers """
    answers = []
    i = 0

    try:
        for xml_answer_item in xml.findall(".//{http://www.imsglobal.org/xsd/ims_qtiasiv1p2}varequal"):
            i += 1
            answers.append(
                {
                    'id': str(i),
                    'text': xml_answer_item.text,
                    'correct': True
                }
            )
    except OSError as e:
        logger.error("%s", e)
    except etree.ParseError as e:
        logger.error("XML parser error: %s", e)
    return answers