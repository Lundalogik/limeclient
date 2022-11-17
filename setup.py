#!/usr/bin/env python
from setuptools import setup

setup(
    name='limeclient',
    version='1.1.2',
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

    install_requires=['requests>=2.4.3'],

    tests_require=['nose>=1.3.3',
                   'describe_it>=1.1.0',
                   'responses>=0.3.0',
                   'pyhamcrest>=1.8.1'],
    test_suite='nose.collector'
)
