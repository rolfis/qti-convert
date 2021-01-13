#!/usr/bin/env python3
"""
QTI to other formats converter
"""

__author__ = "Rolf Johansson"
__version__ = "0.1.0"
__license__ = "Apache"

import argparse
from logzero import logger
from lxml import etree

qti_resource = {}

def main(args):
    """ Main entry point of the app """
    logger.info("Main program starting point.")
    logger.info(args)

    xml_doc = etree.parse(args.filename)

    for xml_resource in xml_doc.getroot().findall(".//{http://www.imsglobal.org/xsd/imsccv1p1/imscp_v1p1}resource[@type='imsqti_xmlv1p2']"):
        this_resource_id = xml_resource.get("identifier")
        qti_resource[this_resource_id] = {}
        qti_resource[this_resource_id]['id'] = this_resource_id
        qti_resource[this_resource_id]['href'] = xml_resource.find("{http://www.imsglobal.org/xsd/imsccv1p1/imscp_v1p1}file").get("href")
        qti_resource[this_resource_id]['title'] = etree.parse(qti_resource[xml_resource.get("identifier")]['href']).getroot().find("{http://www.imsglobal.org/xsd/ims_qtiasiv1p2}assessment").get("title")
        qti_resource[this_resource_id]['items'] = {}

        for xml_item in etree.parse(qti_resource[xml_resource.get("identifier")]['href']).getroot().findall(".//{http://www.imsglobal.org/xsd/ims_qtiasiv1p2}item"):
            this_item_id = xml_item.get("ident")
            qti_resource[this_resource_id]['items'][this_item_id] = {}
            qti_resource[this_resource_id]['items'][this_item_id]['id'] = this_item_id
            qti_resource[this_resource_id]['items'][this_item_id]['title'] = xml_item.find("{http://www.imsglobal.org/xsd/ims_qtiasiv1p2}presentation/{http://www.imsglobal.org/xsd/ims_qtiasiv1p2}material/{http://www.imsglobal.org/xsd/ims_qtiasiv1p2}mattext").text

    for assessment in qti_resource:
        a = qti_resource[assessment]
        print(a['id'] + " " + a['title'])
        for item in a['items']:
            i = a['items'][item]
            print(i['id'] + i['title'])
    

if __name__ == "__main__":
    """ This is executed when run from the command line """
    parser = argparse.ArgumentParser(description="Convert QTI files into other formats.")

    # Input file
    parser.add_argument("filename", help="QTI input file")

    # Optional verbosity counter (eg. -v, -vv, -vvv, etc.)
    parser.add_argument(
        "-v",
        "--verbose",
        action="count",
        default=0,
        help="verbosity (-v, -vv, etc)")

    # Specify output of "--version"
    parser.add_argument(
        "--version",
        action="version",
        version="%(prog)s (version {version})".format(version=__version__))

    args = parser.parse_args()
    main(args)