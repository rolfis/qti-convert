#!/usr/bin/env python3
"""
QTI to other formats converter
"""

import argparse
import hashlib
import json
import re
from pathlib import Path

from logzero import logger
from lxml import etree

import config
import formats
from qti_parser import assessment_meta, item

__author__ = config.__author__
__description__ = config.__description__
__license__ = config.__license__
__version__ = config.__version__


def main(args):
    logger.info(__description__)

    try:
        xml_doc = etree.parse(args.input)

        qti_resource = {
            'assessment': []
        } 

        for xml_resource in xml_doc.getroot().findall(".//{http://www.imsglobal.org/xsd/imsccv1p1/imscp_v1p1}resource[@type='imsqti_xmlv1p2']"):
            # allow fully pathed input files using pathlib's Path objects
            input_path = Path(args.input)
            metadata_path = (input_path.parent / xml_resource.get("identifier") / "assessment_meta.xml")

            this_assessment = {
                'id': xml_resource.get("identifier"),
                'metadata': assessment_meta.get_metadata(metadata_path),
                'question': []
            }

            this_assessment_xml = (input_path.parent / this_assessment['id'] / (this_assessment['id'] + ".xml"))
            logger.info(f"this assessment: {this_assessment_xml}")

            for xml_item in (
                etree.parse(str(this_assessment_xml))
                .getroot()
                .findall(".//{http://www.imsglobal.org/xsd/ims_qtiasiv1p2}item")
            ):
                this_assessment['question'].append(item.get_question(xml_item))

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