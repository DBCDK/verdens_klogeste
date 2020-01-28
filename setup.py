#!/usr/bin/env python3

from setuptools import setup

setup(name="verdens-klogeste",
    version="0.1.0",
    package_dir={"": "src"},
    packages=["verdens_klogeste"],
    description="",
    provides=["verdens_klogeste"],
    install_requires=["requests"]
)
