#!/usr/bin/env python

import glob
import logging
import argparse
import markdown2
import os
import sys
import traceback
import codecs
import re

logger = logging.getLogger(__name__)
logging.basicConfig(
    format="[%(asctime)s] [%(levelname)s] - %(message)s",
    level=logging.INFO,
    datefmt="%Y-%m-%d %H:%M:%S")


def create_output_dir(output_dir):
    if not os.path.exists(output_dir):
        os.mkdir(output_dir)
        logger.info("Created directory = %s", output_dir)
    else:
        logger.info("Directory = %s already exists, skipping creating a new one!", output_dir)


def get_files(convert_all):
    files = []

    for f in glob.glob("*.md"):
        files.append(f)

    if convert_all:
        for f in glob.glob("backup/*.md"):
            files.append(f)

    return files


def wrap_with_bootstrap_template(fname, html_toc, html_content):
    template = """
<!doctype html>
<html lang="en">
  <head>
    <!-- Required meta tags -->
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no">

    <!-- Bootstrap CSS -->
    <link rel="stylesheet" href="css/bootstrap.min.css">
    <link rel="stylesheet" href="css/styles.css">
    <title>%s</title>
  </head>
  <body>
    <div class="main container-fluid">
    <h1>%s</h1>
    <div class="toc">
    <h2>Table of Contents</h2>
    %s
    </div>
    <div class="content">%s</div>
    </div>
  </body>
</html>
""" % (fname, fname, html_toc, html_content)

    return template


def gen_html(file_path, output_dir):
    fname_with_ext = os.path.basename(file_path)
    fname, file_extension = os.path.splitext(fname_with_ext)
    link_patterns=[(re.compile(r'((([A-Za-z]{3,9}:(?:\/\/)?)(?:[\-;:&=\+\$,\w]+@)?[A-Za-z0-9\.\-]+(:[0-9]+)?|(?:www\.|[\-;:&=\+\$,\w]+@)[A-Za-z0-9\.\-]+)((?:\/[\+~%\/\.\w\-_]*)?\??(?:[\-\+=&;%@\.\w_]*)#?(?:[\.\!\/\\\w]*))?)'),r'\1')]
    html = markdown2.markdown_path(file_path, extras=["fenced-code-blocks", "tables", "link-patterns", "toc"], link_patterns=link_patterns)
    html_content = wrap_with_bootstrap_template(fname, html.toc_html, html)

    output_path = "%s/%s.html" % (output_dir, fname)
    with codecs.open(output_path, "w", encoding="utf-8") as op:
        op.write(html_content)


if __name__ == "__main__":
    try:
        parser = argparse.ArgumentParser(description="Convert markdown to html files")
        parser.add_argument("--all", action="store_true")

        args = parser.parse_args()
        convert_all = args.all

        output_dir = "./html"
        create_output_dir(output_dir)

        files = get_files(convert_all)
        for f in files:
            try:
                logger.info("Converting %s\r", f)
                gen_html(f, output_dir)
                logger.info("Conversion complete!")
            except Exception as ex:
                traceback.print_exc(file=sys.stdout)
    except Exception as e:
        traceback.print_exc(file=sys.stdout)
