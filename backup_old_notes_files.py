#!/usr/bin/env python

import sys
import traceback
import re
import logging
import glob
import os

from datetime import datetime, timedelta

logger = logging.getLogger(__name__)
logging.basicConfig(
    format="[%(asctime)s] [%(levelname)s] - %(message)s",
    level=logging.INFO,
    datefmt="%Y-%m-%d %H:%M:%S")

NOTE_REPORT_REGEX = re.compile("(\d{4}-\d{2}-\d{2})-to-(\d{4}-\d{2}-\d{2}).*\.(org|pdf|md)")
NOTE_REGULAR_REGEX = re.compile("(\d{4}-\d{2}-\d{2}).*\.(org|md)")
BACKUP_THRESHOLD_DAYS = 7
BACKUP_DIR = "./backup"
BACKUP_REPORTS_DIR = "./backup/reports"


def get_all_note_files():
    file_list = []
    for f in glob.glob("*.org") + glob.glob("*.pdf") + glob.glob("*.md"):
        file_list.append(f)

    return file_list


def valid_date(s):
    return datetime.strptime(s, "%Y-%m-%d").date()


def get_note_file_properties(file_name):
    file_props = {}
    report_match = NOTE_REPORT_REGEX.match(file_name)
    if report_match is not None:
        file_props["name"] = file_name
        file_props["type"] = "report"
        file_props["start_date"] = valid_date(report_match.group(1))
        file_props["end_date"] = valid_date(report_match.group(2))

        return file_props

    regular_match = NOTE_REGULAR_REGEX.match(file_name)
    if regular_match is not None:
        file_props["name"] = file_name
        file_props["type"] = "regular"
        file_props["date"] = valid_date(regular_match.group(1))

        return file_props

    return None


def get_files_to_backup(file_list):
    files_to_backup = []
    today = datetime.now().date()
    backup_threshold_date = today - timedelta(days=BACKUP_THRESHOLD_DAYS)

    for f in file_list:
        file_props = get_note_file_properties(f)
        if file_props is None:
            continue

        note_file_type = file_props["type"]
        if note_file_type == "report" and file_props["end_date"] < backup_threshold_date:
            files_to_backup.append(file_props)
        if note_file_type == "regular" and file_props["date"] < backup_threshold_date:
            files_to_backup.append(file_props)

    return files_to_backup


def create_dir_if_not_exists(dir_name):
    if not os.path.exists(dir_name):
        logger.info("%s doesn't exist, creating it", dir_name)
        os.makedirs(dir_name)


def perform_backup(file_list):
    if len(file_list) < 1:
        logger.info("No file to backup!")
        return

    create_dir_if_not_exists(BACKUP_DIR)
    create_dir_if_not_exists(BACKUP_REPORTS_DIR)

    for file_props in file_list:
        note_file_type = file_props["type"]
        file_name = file_props["name"]
        if note_file_type == "report":
            logger.info("Backing up notes report file = %s to %s", str(file_name), BACKUP_REPORTS_DIR)
            os.rename(file_name, os.path.join(BACKUP_REPORTS_DIR, file_name))
        else:
            logger.info("Backing up note file = %s to %s", str(file_name), BACKUP_DIR)
            os.rename(file_name, os.path.join(BACKUP_DIR, file_name))


def cleanup_tex_files():
    # Cleanup any remaining tex files due to reports
    for f in glob.glob("*.tex"):
        logger.info("Cleaning up tex file = %s", f)
        os.remove(f)


def main():
    file_list = get_all_note_files()
    files_to_backup = get_files_to_backup(file_list)
    perform_backup(files_to_backup)
    cleanup_tex_files()


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        traceback.print_exc(file=sys.stdout)
