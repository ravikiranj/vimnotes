#!/usr/bin/env python

import argparse
import logging
import traceback
import sys
import glob
import subprocess
import os
import re

from datetime import datetime, timedelta

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)
org_mode_compile_notes_pattern = re.compile(".*-to-.*\.org")

def valid_date(s):
    try:
        return datetime.strptime(s, "%Y-%m-%d").date()
    except ValueError:
        msg = "Not a valid date: '{0}'.".format(s)
        raise argparse.ArgumentTypeError(msg)

def get_op_file_basename(start_date, end_date):
    return str(start_date) + "-to-" + str(end_date)

def get_matching_file_list(start_date, end_date):
    date_list = []
    curr_date = start_date
    while (curr_date <= end_date):
        date_list.append(curr_date)
        curr_date += timedelta(days=1)

    if len(date_list) < 1:
        return []

    file_list = []
    for d in date_list:
        for f in glob.glob("*.org"):
            # Skip any previous compiled org notes
            if f.startswith(str(d)) and not org_mode_compile_notes_pattern.match(f):
                file_list.append(f)

    return file_list


def gen_custom_org_file(start_date, end_date):
    file_list = get_matching_file_list(start_date, end_date)
    if len(file_list) < 1:
        logger.info("No matching org files found for date range, exiting!")
        return

    op_file_basename = get_op_file_basename(start_date, end_date)
    op_file = op_file_basename + ".org"
    op_file_path = os.path.join(os.getcwd(),  op_file)

    with open(op_file, "w") as outfile:
        for fname in file_list:
            with open(fname) as infile:
                logger.info("Writing %s to output file", fname)
                outfile.write("** " + fname + "\n")
                outfile.write(infile.read())
                outfile.write("\n")

    logger.info("Output written to %s", op_file)
    logger.info("Generating PDF file")
    status = subprocess.check_output(["emacs", "-nw", "--batch", "--visit=" + op_file_path, "--funcall=org-latex-export-to-pdf"])
    logger.info("PDF written to %s", op_file_basename + ".pdf")

if __name__ == "__main__":
    try:
        parser = argparse.ArgumentParser()
        parser.add_argument("-s", "--startdate", help="Start Date - format YYYY-MM-DD", required=True, type=valid_date)
        parser.add_argument("-e", "--enddate", help="End Date - format YYYY-MM-DD", required=True, type=valid_date)

        args = parser.parse_args() 
        start_date = args.startdate
        end_date = args.enddate

        if start_date > end_date:
            raise Exception("End date %s is earlier than start date %s!!!" % (start_date, end_date))

        gen_custom_org_file(start_date, end_date)
    except:
        traceback.print_exc(file=sys.stdout)

