"""
Multiple Choice
Select one answer from a list of answers
"""

from lxml import etree
from logzero import logger
import re
import hashlib
import config

def get_answers(xml):
    """ Return an array of possible answers """
    answers = []
    correct_answers = []

    for id in xml.findall(".//{http://www.imsglobal.org/xsd/ims_qtiasiv1p2}respcondition[@continue='No']/{http://www.imsglobal.org/xsd/ims_qtiasiv1p2}conditionvar/{http://www.imsglobal.org/xsd/ims_qtiasiv1p2}varequal"):
        correct_answers.append(id.text)

    try:
        for xml_answer_item in xml.findall(".//{http://www.imsglobal.org/xsd/ims_qtiasiv1p2}response_label"):
            image = []
            this_answer = {}
            this_answer['id'] = xml_answer_item.get("ident")
            this_answer['text'] = xml_answer_item.find("{http://www.imsglobal.org/xsd/ims_qtiasiv1p2}material/{http://www.imsglobal.org/xsd/ims_qtiasiv1p2}mattext").text
            this_answer['correct'] = True if xml_answer_item.get("ident") in correct_answers else False
            this_answer['display'] = True
            
            if this_answer['text'].lower().find("<img.*"):
                for match in re.finditer('^<img src="([^"]+)".*>', this_answer['text'], re.DOTALL):
                    image.append({
                        'id': str(hashlib.md5(match.group(1).replace(config.img_href_ims_base, "").encode()).hexdigest()),
                        'href': match.group(1).replace(config.img_href_ims_base, "")
                    })
                p = re.compile('<img src="([^"]+)".*>')
                subn_tuple = p.subn('', this_answer['text'])
                if subn_tuple[1] > 0:
                    this_answer['text'] = subn_tuple[0]

            if image:
                this_answer['image'] = image

            answers.append(this_answer)

    except OSError as e:
        logger.error("%s", e)
    except etree.ParseError as e:
        logger.error("XML parser error: %s", e)
    return answers