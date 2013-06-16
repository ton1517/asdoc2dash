from setuptools import setup

import asdoc2dash

def join_files(*files):
    content = ""
    for name in files:
        f = open(name)
        content += f.read() + "\n"
        f.close()
    return content

setup(
    name = 'asdoc2dash',
    version = asdoc2dash.__version__,
    description = asdoc2dash.__doc__.strip(),
    long_description = join_files("README.rst", "CHANGES.rst"),
    url = asdoc2dash.__homepage__,
    license = asdoc2dash.__license__,
    author = asdoc2dash.__author__,
    author_email = asdoc2dash.__email__,
    packages = ["asdoc2dash"],
    entry_points = {
        "console_scripts": ["asdoc2dash = asdoc2dash.asdoc2dash:main"]
    },
    install_requires = open("requirements.txt").read().splitlines(),
    platforms = 'any',
    classifiers = [
        'Development Status :: 3 - Alpha',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: MacOS :: MacOS X',
        'Topic :: Documentation',
        'Topic :: Software Development',
        'Topic :: Software Development :: Documentation',
        'Topic :: Text Processing'
    ]
)
