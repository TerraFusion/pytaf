from setuptools import setup
from setuptools.extension import Extension
from Cython.Build import cythonize
from Cython.Distutils import build_ext

import numpy

setup(name='pytaf',
      version='0.0.1',
      description='Python wrapper for advanced funsion reprojection',
      author='TerraFusion Team',
      author_email='eoshelp@hdfgroup.org',
      test_suite='nose.collector',
      tests_require=['nose'],      
      cmdclass = {'build_ext':build_ext},
      ext_modules = cythonize([Extension("pytaf",
                                         sources=["pytaf.pyx", "reproject.c"],
                                         include_dirs=[numpy.get_include()])],
                              gdb_debug=True)    
)
