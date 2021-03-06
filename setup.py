"""
setup.py

This script helps you test, install, and package pytaf module in a standard
Python distribution manner.

Usage:

For installation, 

 $python setup.py install

For testing,

 $python setup.py test

Tested under: Python 3.6.6 :: Anaconda custom (64-bit)
Last updated: 2019-04-22
"""
from setuptools import setup
from setuptools.extension import Extension
from Cython.Build import cythonize
from Cython.Distutils import build_ext

import numpy

setup(name='pytaf',
      version='1.0.0',
      description='Python wrapper for advanced funsion reprojection',
      author='TerraFusion Team',
      author_email='eoshelp@hdfgroup.org',
      url = 'https://github.com/TerraFusion',
      test_suite='nose.collector',
      tests_require=['nose'],      
      cmdclass = {'build_ext':build_ext},
      ext_modules = cythonize([Extension("pytaf",
                                         sources=["pytaf.pyx", "reproject.c"],
                                         include_dirs=[numpy.get_include()])],
                              gdb_debug=True)    
)
