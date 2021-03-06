#!/usr/bin/env python3

import glob
from setuptools import setup, find_packages

setup(name="verdens_klogeste",
    version="0.1.0",
    package_dir={"": "src"},
    packages=find_packages(where='src'),
    description="",
    scripts=glob.glob('src/bin/*'),
    install_requires=["dbc-pyutils", "requests", "rrflow", "ibm-watson>=4.2.1", "Wikipedia-API", "sklearn", "tornado"],
    include_package_data=True,
    provides=["verdens_klogeste"],
    zip_safe=False,
    entry_points=
        {"console_scripts": [
            "verdens-klogeste-service = verdens_klogeste.service:main",
        ]}
)
