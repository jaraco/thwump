# -*- coding: UTF-8 -*-

"""
Setup script for building thwump distribution

Copyright © 2011-2012 Jason R. Coombs
"""

from setuptools import find_packages

name = 'thwump'

setup_params = dict(
	name = name,
	use_hg_version=True,
	description = 'A MongoDB backend for Whoosh',
	long_description = open('README').read(),
	author = 'Jason R. Coombs',
	author_email = 'jaraco@jaraco.com',
	url = 'http://pypi.python.org/pypi/'+name,
	packages = find_packages(),
	license = 'MIT',
	classifiers = [
		"Intended Audience :: Developers",
		"Programming Language :: Python",
		"Programming Language :: Python :: 3",
	],
	entry_points = {
		'console_scripts': [
			],
	},
	install_requires=[
		'pymongo',
	],
	extras_require = {
	},
	dependency_links = [
	],
	tests_require=[
		'whoosh',
	],
	setup_requires=[
		'hgtools>=1.0',
		'pytest-runner',
	],
	use_2to3=True,
)

if __name__ == '__main__':
	from setuptools import setup
	setup(**setup_params)
