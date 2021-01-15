#!/usr/bin/env python3
"""
QTI to other formats converter
"""

__author__ = "Rolf Johansson"
__version__ = "0.1.0"
__license__ = "Apache"

from qti_parser import question_type
import argparse
import json
from logzero import logger
from lxml import etree

qti_resource = {
    'assessment': []
} 

def main(args):
    """ Main entry point of the app """
    logger.info("QTI converter utility.")
    logger.info(args)

    try:
        xml_doc = etree.parse(args.input)

        for xml_resource in xml_doc.getroot().findall(".//{http://www.imsglobal.org/xsd/imsccv1p1/imscp_v1p1}resource[@type='imsqti_xmlv1p2']"):
            this_assessment = {
                'id': xml_resource.get("identifier"), 
                'title': '', 
                'question': []
            }
            this_assessment_xml = this_assessment['id'] + "/" + this_assessment['id'] + ".xml"

            for xml_item in etree.parse(this_assessment_xml).getroot().findall(".//{http://www.imsglobal.org/xsd/ims_qtiasiv1p2}item"):
                xml_item_metadata = xml_item.find("{http://www.imsglobal.org/xsd/ims_qtiasiv1p2}itemmetadata/{http://www.imsglobal.org/xsd/ims_qtiasiv1p2}qtimetadata")
                this_question = {
                    'id': str(xml_item.get("ident")),
                    'question_type': xml_item_metadata.find("{http://www.imsglobal.org/xsd/ims_qtiasiv1p2}qtimetadatafield[{http://www.imsglobal.org/xsd/ims_qtiasiv1p2}fieldlabel = 'question_type']/{http://www.imsglobal.org/xsd/ims_qtiasiv1p2}fieldentry").text,
                    'points_possible': xml_item_metadata.find("{http://www.imsglobal.org/xsd/ims_qtiasiv1p2}qtimetadatafield[{http://www.imsglobal.org/xsd/ims_qtiasiv1p2}fieldlabel = 'points_possible']/{http://www.imsglobal.org/xsd/ims_qtiasiv1p2}fieldentry").text,
                    'text': xml_item.find("{http://www.imsglobal.org/xsd/ims_qtiasiv1p2}presentation/{http://www.imsglobal.org/xsd/ims_qtiasiv1p2}material/{http://www.imsglobal.org/xsd/ims_qtiasiv1p2}mattext").text
                }

                if this_question['question_type'] == "multiple_choice_question":
                    this_question['answer'] = question_type.multiple_choice.get_answers(xml_item)
                elif this_question['question_type'] == "true_false_question":
                    this_question['answer'] = question_type.true_false.get_answers(xml_item)
                elif this_question['question_type'] == "multiple_answers_question":
                    this_question['answer'] = question_type.multiple_answers.get_answers(xml_item)
                elif this_question['question_type'] == "short_answer_question":
                    this_question['answer'] = question_type.short_answer.get_answers(xml_item)

                this_assessment['question'].append(this_question)
                this_assessment['title'] = etree.parse(this_assessment_xml).getroot().find("{http://www.imsglobal.org/xsd/ims_qtiasiv1p2}assessment").get("title")

            qti_resource['assessment'].append(this_assessment)

        qti_resource_json = json.dumps(qti_resource, indent = 2)
        print(qti_resource_json)

    except OSError as e:
        logger.error("%s", e)

    except etree.ParseError as e:
        logger.error("XML parser error: %s", e)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Convert QTI files into other formats.", add_help=False)
    parser.add_argument("input", help="QTI input file.")
    parser.add_argument("-v", action="count", default=0, help="Verbosity (-v, -vv, etc).")
    parser.add_argument("-f", action="store", dest="format", default="json", help="Output format, defaults to JSON.")
    parser.add_argument( "--version", action="version", help="Display version and exit.", version="%(prog)s (version {version})".format(version=__version__))
    parser.add_argument('-h', '--help', action='help', default=argparse.SUPPRESS, help='Show this help message and exit.')
    args = parser.parse_args()
    print(args)
    main(args)