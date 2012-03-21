from setuptools import setup, find_packages
import sys, os
from distutils.core import Command
from unittest import TextTestRunner, TestLoader
from glob import glob
from os.path import splitext, basename, join as pjoin, walk
import doctest

def read(f):
    return open(f).read()

version = read(os.path.join('w20e', 'forms', 'version.txt')).strip()
long_descr = ".. contents:: Table of Contents\n\n" + \
    read(os.path.join('README.txt')) + '\n\n' + \
    read(os.path.join('w20e', 'forms', 'xml', 'README.txt')) + '\n\n' + \
    read(os.path.join('w20e', 'forms', 'pyramid', 'README.txt'))


class TestCommand(Command):
    user_options = [ ]

    def initialize_options(self):
        self._dir = os.getcwd()

    def finalize_options(self):
        pass

    def run(self):
        '''
        Finds all the tests modules in tests/, and runs them.
        '''
        testfiles = [ ]
        for t in glob(pjoin(self._dir, 'tests', '*.py')):
            if not t.endswith('__init__.py'):
                testfiles.append('.'.join(
                    ['tests', splitext(basename(t))[0]])
                )

        print testfiles

        tests = TestLoader().loadTestsFromNames(testfiles)
        t = TextTestRunner(verbosity = 1)
        t.run(tests)

        doctest.testmod()
        doctest.testfile("README.txt")


setup(name='w20e.forms',
      version=version,
      description="Python API for creating and handling forms",
      long_description=long_descr,
      classifiers=[
        "Development Status :: 4 - Beta",
        "Framework :: Plone",
        "Framework :: Pylons",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: GNU General Public License (GPL)",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        ],
      keywords='forms',
      author='D.A.Dokter',
      author_email='dokter@w20e.com',
      url='',
      license='GPL',
      packages=find_packages(exclude=['ez_setup', 'examples']),
      include_package_data=True,
      zip_safe=False,
      install_requires=[
        'lxml',
        'zope.interface',
        'ordereddict',
        'Chameleon',
      ],
      entry_points="""
      # -*- Entry points: -*-
      """,
      cmdclass = { 'test': TestCommand }

      )
