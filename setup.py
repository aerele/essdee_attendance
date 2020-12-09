# -*- coding: utf-8 -*-
from setuptools import setup, find_packages

with open('requirements.txt') as f:
	install_requires = f.read().strip().split('\n')

# get version from __version__ variable in essdee_attendance/__init__.py
from essdee_attendance import __version__ as version

setup(
	name='essdee_attendance',
	version=version,
	description='Frappe application to track attendance',
	author='Aerele',
	author_email='admin@aerele.in',
	packages=find_packages(),
	zip_safe=False,
	include_package_data=True,
	install_requires=install_requires
)
