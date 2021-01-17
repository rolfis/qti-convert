"""
Calculated Answer
"""

from lxml import etree
from logzero import logger
import re
import config

def get_answers(xml):
    """ Return an array of possible answers and their variable substitution """
    var_sets = []
    tolerance = 0

    try:
        if xml.find("{http://www.imsglobal.org/xsd/ims_qtiasiv1p2}answer_tolerance") is not None:
            tolerance = xml.find("{http://www.imsglobal.org/xsd/ims_qtiasiv1p2}answer_tolerance")
        for xml_var_set in xml.findall(".//{http://www.imsglobal.org/xsd/ims_qtiasiv1p2}var_set"):
            this_var_set = {
                'id': xml_var_set.get("ident"),
                'value': xml_var_set.find("{http://www.imsglobal.org/xsd/ims_qtiasiv1p2}answer").text,
                'text': "",
                'display': True,
                'correct': True,
                'tolerance': tolerance,
                'variable': []
            }
            for xml_var_set_variable in xml_var_set.findall(".//{http://www.imsglobal.org/xsd/ims_qtiasiv1p2}var"):
                this_var_set['variable'].append({
                    'name': xml_var_set_variable.get("name"),
                    'value': xml_var_set_variable.text
                })
                if this_var_set['text'] == "":
                    this_var_set['text'] = xml_var_set_variable.get("name") + " = " + xml_var_set_variable.text
                else:
                    this_var_set['text'] = this_var_set['text'] + ", " + xml_var_set_variable.get("name") + " = " + xml_var_set_variable.text
            var_sets.append(this_var_set)
            
    except OSError as e:
        logger.error("%s", e)
    except etree.ParseError as e:
        logger.error("XML parser error: %s", e)
    return var_sets

def substitute_variables_in_question(text, answer):
    """ Clarify variable placeholders in question text """
    start = 0
    newstring = ""
    placeholder_regex = r"\[(.*?)\]"
    for m in re.finditer(placeholder_regex, text):
        end, newstart = m.span()
        newstring += text[start:end]
        for var in answer['variable']:
            if var['name'] == m.group(1):
                rep = var['value']
        newstring += rep
        start = newstart
    return newstring
