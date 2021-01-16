#!/usr/bin/env python3
"""
QTI to other formats converter
"""

import formats
import argparse
import json
import re
import hashlib
from logzero import logger
from lxml import etree
from qti_parser import question_type
import config

__author__ = config.__author__
__description__ = config.__description__
__license__ = config.__license__
__version__ = config.__version__

def main(args):
    logger.info(__description__)
    logger.info(args)

    try:
        xml_doc = etree.parse(args.input)

        qti_resource = {
            'assessment': []
        } 

        for xml_resource in xml_doc.getroot().findall(".//{http://www.imsglobal.org/xsd/imsccv1p1/imscp_v1p1}resource[@type='imsqti_xmlv1p2']"):
            this_assessment = {
                'id': xml_resource.get("identifier"), 
                'title': '', 
                'question': []
            }

            # TODO: Should be prefixed with PATH part of input filename since paths in XML are relative
            this_assessment_xml = this_assessment['id'] + "/" + this_assessment['id'] + ".xml"

            for xml_item in etree.parse(this_assessment_xml).getroot().findall(".//{http://www.imsglobal.org/xsd/ims_qtiasiv1p2}item"):
                xml_item_metadata = xml_item.find("{http://www.imsglobal.org/xsd/ims_qtiasiv1p2}itemmetadata/{http://www.imsglobal.org/xsd/ims_qtiasiv1p2}qtimetadata")
                this_question = {
                    'id': str(xml_item.get("ident")),
                    'question_type': xml_item_metadata.find("{http://www.imsglobal.org/xsd/ims_qtiasiv1p2}qtimetadatafield[{http://www.imsglobal.org/xsd/ims_qtiasiv1p2}fieldlabel = 'question_type']/{http://www.imsglobal.org/xsd/ims_qtiasiv1p2}fieldentry").text,
                    'points_possible': xml_item_metadata.find("{http://www.imsglobal.org/xsd/ims_qtiasiv1p2}qtimetadatafield[{http://www.imsglobal.org/xsd/ims_qtiasiv1p2}fieldlabel = 'points_possible']/{http://www.imsglobal.org/xsd/ims_qtiasiv1p2}fieldentry").text,
                    'text': xml_item.find("{http://www.imsglobal.org/xsd/ims_qtiasiv1p2}presentation/{http://www.imsglobal.org/xsd/ims_qtiasiv1p2}material/{http://www.imsglobal.org/xsd/ims_qtiasiv1p2}mattext").text
                }

                image = []

                # Try and find images in text
                if this_question['text'].lower().find("<p>.*<img"):
                    for match in re.finditer('<p>.*<img src=\"([^\"]+)\".*>.*</p>', this_question['text'], re.DOTALL):
                        this_href = re.sub("\?.+$", "", match.group(1)).replace(config.img_href_ims_base, "")
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
                        this_href = re.sub("\?.+$", "", match.group(1)).replace(config.img_href_ims_base, "")
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

                if (this_question['question_type'] == "fill_in_multiple_blanks_question" or this_question['question_type'] == "multiple_dropdowns_question") and this_question['text'].find("\[(.*?)\]"):
                    p = re.compile("\[(.*?)\]")
                    subn_tuple = p.subn(config.blanks_replace * config.blanks_replace_n, this_question['text'])
                    if subn_tuple[1] > 0:
                        this_question['text'] = subn_tuple[0]

                this_assessment['question'].append(this_question)
                this_assessment['title'] = etree.parse(this_assessment_xml).getroot().find("{http://www.imsglobal.org/xsd/ims_qtiasiv1p2}assessment").get("title")

            qti_resource['assessment'].append(this_assessment)

        if args.format.lower() == "json":
            if args.output:
                logger.info("Writing JSON to '" + args.output + "'...")
                with open(args.output, 'w') as outfile:
                    json.dump(qti_resource, outfile)
            else:
                logger.info("Writing JSON to STDOUT...")
                qti_resource_json = json.dumps(qti_resource, indent = 2)
                print(qti_resource_json)

        elif args.format.lower() == "docx":
            if args.output:
                outfile = args.output
            else:
                outfile = "output.docx"
            logger.info("Writing DOCX to '" + outfile + "'...")
            formats.docx.write_file(qti_resource, outfile)

        elif args.format.lower() == "pdf":
            logger.error("Format not supported yet: " + args.format)

        else:
            logger.error("Unknown format: " + args.format)

    except OSError as e:
        logger.error("%s", e)

    except etree.ParseError as e:
        logger.error("XML parser error: %s", e)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Convert QTI files into other formats.", add_help=False)
    parser.add_argument("input", help="QTI input file (imsmanifest.xml).")
    parser.add_argument("-v", action="count", default=0, help="Verbosity (-v, -vv, etc).")
    parser.add_argument("-f", action="store", dest="format", default="json", help="Output format, defaults to JSON.")
    parser.add_argument("-o", action="store", dest="output", help="Output file.")
    parser.add_argument( "--version", action="version", help="Display version and exit.", version="%(prog)s (version {version})".format(version=__version__))
    parser.add_argument('-h', '--help', action='help', default=argparse.SUPPRESS, help='Show this help message and exit.')
    args = parser.parse_args()
    main(args)