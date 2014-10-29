#!/usr/bin/env python
from setuptools import setup, find_packages

setup(
    name='limeclient',
    version='0.0.4',
    description='Python client for the LIME Pro API',
    classifiers=[
        'Development Status :: 4 - Beta',
        'License :: OSI Approved :: Mozilla Public License 2.0 (MPL 2.0)',
        'Programming Language :: Python :: 3'
    ],
    author='Lundalogik AB',
    author_email='info@lundalogik.se',
    license='MPL 2.0',

    packages=['limeclient'],
    include_package_data=True,

    install_requires=['requests>=2.4.3']
)
