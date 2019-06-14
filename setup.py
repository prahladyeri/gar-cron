#!/usr/bin/env python3
import os
import gar_cron
from setuptools import setup, find_packages

def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

s = setup(
	name='gar-cron',
	version=gar_cron.__version__,
	license='MIT',
	description=gar_cron.__title__,
	long_description=read("README.md"),
	long_description_content_type='text/markdown',
	keywords="internet",
	url='https://github.com/prahladyeri/gar-cron',
	packages=find_packages(),
	include_package_data=True,
	entry_points={
		"console_scripts": [
			"gar-cron = gar_cron.cron:main",
		],
	},
	install_requires=['requests'],
	author='Prahlad Yeri',
	author_email='prahladyeri@yahoo.com',
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
	)
