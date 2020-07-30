#!/usr/bin/env python

from setuptools import setup, find_packages

setup(
    name='Fido2 Flask Credential Storage',
    version='1.0',
    long_description=__doc__,
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        'Flask',
        'sqlalchemy',
        'fido2',
    ],
    extras_require={
        'mysql': ['pymysql'],
    }
)
