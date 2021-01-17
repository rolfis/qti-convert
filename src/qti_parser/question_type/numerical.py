"""
Numerical Answer
"""

from lxml import etree
from logzero import logger

def get_answers(xml):
    """ Return an array of possible answers """
    answers = []
    i = 0

    try:
        for xml_cond in xml.findall(".//{http://www.imsglobal.org/xsd/ims_qtiasiv1p2}conditionvar"):
            i += 1
            value, minvalue, maxvalue = None, None, None
            if xml_cond.find("{http://www.imsglobal.org/xsd/ims_qtiasiv1p2}or/{http://www.imsglobal.org/xsd/ims_qtiasiv1p2}varequal") is not None:
                value = xml_cond.find("{http://www.imsglobal.org/xsd/ims_qtiasiv1p2}or/{http://www.imsglobal.org/xsd/ims_qtiasiv1p2}varequal").text
                minvalue = value
                maxvalue = value
            if xml_cond.find("{http://www.imsglobal.org/xsd/ims_qtiasiv1p2}or/{http://www.imsglobal.org/xsd/ims_qtiasiv1p2}and") is not None:
                xml_cond_range = xml_cond.find("{http://www.imsglobal.org/xsd/ims_qtiasiv1p2}or/{http://www.imsglobal.org/xsd/ims_qtiasiv1p2}and")
            if xml_cond.find("{http://www.imsglobal.org/xsd/ims_qtiasiv1p2}vargte") is not None or xml_cond.find("{http://www.imsglobal.org/xsd/ims_qtiasiv1p2}varlte") is not None:
                xml_cond_range = xml_cond
            if xml_cond_range.find("{http://www.imsglobal.org/xsd/ims_qtiasiv1p2}vargte") is not None:
                minvalue = xml_cond_range.find("{http://www.imsglobal.org/xsd/ims_qtiasiv1p2}vargte").text
            elif xml_cond_range.find("{http://www.imsglobal.org/xsd/ims_qtiasiv1p2}vargt") is not None:
                minvalue = xml_cond_range.find("{http://www.imsglobal.org/xsd/ims_qtiasiv1p2}vargt").text
            if xml_cond_range.find("{http://www.imsglobal.org/xsd/ims_qtiasiv1p2}varlte") is not None:
                maxvalue = xml_cond_range.find("{http://www.imsglobal.org/xsd/ims_qtiasiv1p2}varlte").text
            elif xml_cond_range.find("{http://www.imsglobal.org/xsd/ims_qtiasiv1p2}varlt") is not None:
                maxvalue = xml_cond_range.find("{http://www.imsglobal.org/xsd/ims_qtiasiv1p2}varlt").text
            this_answer = {}
            this_answer['id'] = str(i)
            if value is not None:
                this_answer['value'] = value
            if minvalue is not None:
                this_answer['minvalue'] = minvalue
            if maxvalue is not None:
                this_answer['maxvalue'] = maxvalue
            this_answer['correct'] = True
            this_answer['display'] = False
            answers.append(this_answer)
            
    except OSError as e:
        logger.error("%s", e)
    except etree.ParseError as e:
        logger.error("XML parser error: %s", e)
    return answers