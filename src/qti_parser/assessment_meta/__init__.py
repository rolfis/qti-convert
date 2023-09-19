"""
Assesment Metadata
"""

from lxml import etree
from logzero import logger


def get_metadata(file_path):
    """ Extracts basic metadata """
    metadata = {}

    try:
        xml = etree.parse(str(file_path)).getroot()
        metadata = {
            'title': xml.find("./{http://canvas.instructure.com/xsd/cccv1p0}title").text,
            'description': xml.find("./{http://canvas.instructure.com/xsd/cccv1p0}description").text,
            'type': xml.find("./{http://canvas.instructure.com/xsd/cccv1p0}quiz_type").text,
            'points_possible': xml.find("./{http://canvas.instructure.com/xsd/cccv1p0}points_possible").text
        }

    except OSError as e:
        logger.error("%s", e)

    except etree.ParseError as e:
        logger.error("XML parser error: %s", e)

    return metadata
