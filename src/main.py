#!/usr/bin/env python3
"""
QTI to other formats converter
"""

__author__ = "Rolf Johansson"
__version__ = "0.1.0"
__license__ = "Apache"

import argparse
import json
from logzero import logger
from lxml import etree

qti_resource = {
    'assessments': []
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
                'questions': []
            }
            this_assessment_xml = this_assessment['id'] + "/" + this_assessment['id'] + ".xml"

            for xml_item in etree.parse(this_assessment_xml).getroot().findall(".//{http://www.imsglobal.org/xsd/ims_qtiasiv1p2}item"):
                this_question = {
                    'id': xml_item.get("ident"), 
                    'text': xml_item.find("{http://www.imsglobal.org/xsd/ims_qtiasiv1p2}presentation/{http://www.imsglobal.org/xsd/ims_qtiasiv1p2}material/{http://www.imsglobal.org/xsd/ims_qtiasiv1p2}mattext").text,
                    'answers': []
                }
                this_assessment['questions'].append(this_question)
                this_assessment['title'] = etree.parse(this_assessment_xml).getroot().find("{http://www.imsglobal.org/xsd/ims_qtiasiv1p2}assessment").get("title")

                # multiple_choice_question
                # short_answer_question

            qti_resource['assessments'].append(this_assessment)

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