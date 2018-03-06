#!/usr/bin/env python

import sys
import traceback
import logging
import os

from datetime import datetime

logger = logging.getLogger(__name__)
logging.basicConfig(
    format="[%(asctime)s] [%(levelname)s] - %(message)s",
    level=logging.INFO,
    datefmt="%Y-%m-%d %H:%M:%S")


def main():
    today = datetime.now().date()
    todays_org_file_name = "./" + today.strftime("%Y-%m-%d") + ".org"
    if os.path.isfile(todays_org_file_name):
        logger.info("%s already exists, not creating it", todays_org_file_name)
    else:
        logger.info("Creating %s", todays_org_file_name)
        with open(todays_org_file_name, "w"):
            pass
        logger.info("Done")


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        traceback.print_exc(file=sys.stdout)
