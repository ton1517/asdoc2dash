asdoc2dash
==========

asdoc2dash is tools that convert from ASDoc(ActionScript Documentation) to `Dash <http://kapeli.com/dash>`_ Docset.

installation
------------
install from pypi

::

    easy_install asdoc2dash

or

::

    pip install asdoc2dash


install from github

::

    git clone git@github.com:ton1517/asdoc2dash.git
    python setup.py install

usage
------
::

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

example
-------
add my library's asdoc to Dash.
::

    asdoc2dash --name mylib --docdir ./mylib/doc/ --add-to-dash

