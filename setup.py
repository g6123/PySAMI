# -*- coding: utf-8 -*- #

from sys import version_info
if version_info.major < 3:
	print('Cumulus is not compatible under Python 2.')
	exit()

from distutils.core import setup
setup(
	name='pysami', version='0.1.5',
	packages=['pysami'], package_dir={ 'pysami': 'src' },
	author='유성매직', author_email='유성매직 <g6123@cys.wo.tc>',
	description='Python library and script for converting SAMI file.',
	url='https://github.com/g6123/pysami', license='MIT License',
) 
