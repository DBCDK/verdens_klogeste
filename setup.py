#!/usr/bin/env python3

import glob
from setuptools import setup, find_packages

setup(name="verdens-klogeste",
    version="0.1.0",
    package_dir={"": "src"},
    packages=find_packages(where='src'),
    description="",
    scripts=glob.glob('src/bin/*'),
    provides=["verdens_klogeste"],
    install_requires=["requests", "ibm-watson>=4.2.1", "Wikipedia-API", "sklearn"]
)
