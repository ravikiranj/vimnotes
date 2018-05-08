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
compile_notes_pattern = re.compile(".*-to-.*\.(org|md)")
notes_mode = ".md"


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
        for f in glob.glob("*" + notes_mode):
            # Skip any previous compiled notes
            if f.startswith(str(d)) and not compile_notes_pattern.match(f):
                file_list.append(f)

    return file_list


def gen_custom_note_file(start_date, end_date):
    file_list = get_matching_file_list(start_date, end_date)
    if len(file_list) < 1:
        logger.info("No matching note files found for date range, exiting!")
        return

    op_file_basename = get_op_file_basename(start_date, end_date)
    op_file = op_file_basename + notes_mode
    op_file_path = os.path.join(os.getcwd(),  op_file)

    with open(op_file, "w") as outfile:
        for fname in file_list:
            with open(fname) as infile:
                logger.info("Writing %s to output file", fname)
                if notes_mode == ".org":
                    outfile.write("** " + fname + "\n")
                else:
                    outfile.write("## " + fname + "\n")

                outfile.write(infile.read())
                outfile.write("\n")

    logger.info("Output written to %s", op_file)
    logger.info("Generating PDF file")
    if notes_mode == ".org":
        subprocess.check_output(["emacs", "-nw", "--batch", "--visit=" + op_file_path, "--funcall=org-latex-export-to-pdf"])
        logger.info("PDF written to %s", op_file_basename + ".pdf")
    else:
        if cmd_exists("markdown-toc"):
            toc = subprocess.check_output(["markdown-toc", op_file_path])
            with file(op_file_path, 'r') as original:
                data = original.read()
                toc_heading = "# Table of Contents"
                with file(op_file_path, 'w') as modified:
                    modified.write(toc_heading + "\n\n" + toc + "\n\n" + data)
                    logger.info("Wrote table of contents to markdown file")
        else:
            logger.info("markdown-toc is not installed, hence not writing table of contents")
        if cmd_exists("markdown-pdf"):
            subprocess.check_output(["markdown-pdf", op_file_path])
            logger.info("PDF written to %s", op_file_basename + ".pdf")
        else:
            logger.error("Please install markdown-pdf via 'npm install -g markdown-pdf'")


def cmd_exists(cmd):
    return subprocess.call("type " + cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE) == 0


if __name__ == "__main__":
    try:
        logger.info("Notes mode = %s", notes_mode)
        parser = argparse.ArgumentParser()
        parser.add_argument("-s", "--startdate", help="Start Date - format YYYY-MM-DD", required=True, type=valid_date)
        parser.add_argument("-e", "--enddate", help="End Date - format YYYY-MM-DD", required=True, type=valid_date)

        args = parser.parse_args()
        start_date = args.startdate
        end_date = args.enddate

        if start_date > end_date:
            raise Exception("End date %s is earlier than start date %s!!!" % (start_date, end_date))

        gen_custom_note_file(start_date, end_date)
    except:
        traceback.print_exc(file=sys.stdout)
