#! /usr/bin/env python
# -*- coding: utf-8 -*-


try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

DISTNAME = "rrr"
DESCRIPTION = "A set of python modules to retrieve related relationships"
# with open("README.rst") as f:
#     LONG_DESCRIPTION = f.read()
AUTHOR = "Sosuke Kato"
AUTHOR_EMAIL = "snoopies.drum@gmail.com"
URL = "https://github.com/knowledge-retrieval/3r"
LICENSE = "MIT"
PACKAGES = ["rrr"]
PACKAGE_DIR = {"rrr": "rrr"}
# SCRIPTS = ["scripts/generate-mdcorpus-database.py"]

import rrr
VERSION = rrr.__version__

DEPENDENCIES = [
    "Flask==0.12",
]


def setup_package():
    metadata = dict(name=DISTNAME,
                    description=DESCRIPTION,
                    author=AUTHOR,
                    author_email=AUTHOR_EMAIL,
                    license=LICENSE,
                    url=URL,
                    version=VERSION,
                    # long_description=LONG_DESCRIPTION,
                    packages=PACKAGES,
                    install_requires=DEPENDENCIES,
                    package_dir=PACKAGE_DIR,
                    # scripts=SCRIPTS,
                    )

    setup(**metadata)


if __name__ == "__main__":
    setup_package()
