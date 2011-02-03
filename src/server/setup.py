from setuptools import setup
import os
import sys

def find_packages(dir_):
    packages = []
    for _dir, subdirectories, files in os.walk(os.path.join(dir_, 'geo')):
        if '__init__.py' in files:
            lib, fragment = _dir.split(os.sep, 1)
            packages.append(fragment.replace(os.sep, '.'))
    return packages


setup(name='geo-data-proxy',
	version='1.0',  
	description='Geo Abstraction Library',  
	author='Rodolfo Barriga',  
	author_email='rodolfo.barriga@gmail.com',  
	url='',  
	license='GPL',
	packages = find_packages('lib'),
	package_dir = {'':'lib'}
)