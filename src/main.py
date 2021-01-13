#!/usr/bin/env python3
"""
QTI to other formats converter
"""

__author__ = "Rolf Johansson"
__version__ = "0.1.0"
__license__ = "Apache"

import argparse
from logzero import logger

def main(args):
    """ Main entry point of the app """
    logger.info("Main program starting point.")
    logger.info(args)


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