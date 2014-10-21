#!/usr/bin/env python
from setuptools import setup, find_packages

setup(
    name='limeclient',
    version='0.0.1',
    packages=find_packages(),
    include_package_data=True,

    install_requires=['requests>=2.4.3']
)

