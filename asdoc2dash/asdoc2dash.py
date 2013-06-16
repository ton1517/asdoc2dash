"""asdoc2dash
Convert form ASDoc to Dash Docset.

Usage:
  asdoc2dash --name <name> --docdir <path> (--outdir <path>|--add-to-dash) [--icon <path>] [--force] [--log]
  asdoc2dash (-h | --help)
  asdoc2dash (-v | --version)

Options:
  -h --help           show help.
  -v --version        show version.
  -n --name <name>    docset name
  -d --docdir <path>  asdoc directory
  -o --outdir <path>  output directory
  -a --add-to-dash    add to dash
  -f --force          if exists directory, force overwrite
  -i --icon <path>    docset icon (png format only)
  -l --log            show debug information

"""

import os
import sys
import errno
import shutil
import logging

from . import __author__, __version__, __license__
from . import __doc__ as __description__

from docopt import docopt

import dash
from dash import DocsetGenerator
from asdocparser import ASDocParser

log = logging.getLogger(__name__)


def main():
    arguments = docopt(__doc__, version=__version__)

    docset_name = arguments["--name"]
    asdocdir = arguments["--docdir"]
    outdir = arguments["--outdir"]
    icon = arguments["--icon"]
    add_dash_flag = arguments["--add-to-dash"]

    if add_dash_flag:
        outdir = os.path.join(dash.DEFAULT_DOCSET_PATH, docset_name)

    docset_path = os.path.join(outdir, docset_name + ".docset")

    # log settings
    if arguments["--log"]:
        logging.basicConfig(format="%(asctime)s: %(levelname)s\n%(message)s", level=logging.DEBUG)
    else:
        logging.basicConfig(format="%(message)s", level=logging.INFO)

    # error check
    if not os.path.exists(asdocdir):
        log.error("Not such directory " + asdocdir)
        sys.exit(errno.ENOENT)

    if not os.path.isdir(asdocdir):
        log.error("Not a directory " + asdocdir)
        sys.exit(errno.ENOTDIR) 

    if os.path.exists(docset_path):
        if arguments["--force"]:
            shutil.rmtree(docset_path)
        else:
            log.error("Already exists " + docset_path + "\nIf you want to overwrite, use option --force.")
            sys.exit(errno.EEXIST)

    if icon:
        if not os.path.exists(icon):
            log.error("Not such file " + icon)
            sys.exit(errno.ENOENT)

        filename, ext = os.path.splitext(icon)
        ext = ext.lower()

        if ext != ".png":
            log.error("Icon is supported only png")
            sys.exit(1)

    # main

    log.info("convert from %s to %s", asdocdir, docset_path)

    generator = DocsetGenerator(docset_name, docset_path, asdocdir, icon)
    asdocParser = ASDocParser(generator)

    generator.create_project()
    asdocParser.parse()
    generator.finish()

    log.info("done.")

    # add to dash
    if add_dash_flag:
        log.info("add to dash")
        os.system("open -a dash '%s'" % docset_path)

if __name__ == '__main__':
    main()
