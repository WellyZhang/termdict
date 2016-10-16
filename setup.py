#!/usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import setup, find_packages
from termdict.config import VERSION

setup(name='termdict',
      version=VERSION,
      description="A Parsing-based Terminal Dictionary Framework",
      author='WellyZhang',
      author_email='wellyzhangc@gmail.com',
      url='http://wellyzhang.github.io',
      license='MIT',
      packages=find_packages(),
      include_package_data=True,
      zip_safe=False,
      classifiers=[
          'Programming Language :: Python :: 2',
          'Programming Language :: Python :: 2.6',
          'Programming Language :: Python :: 2.7',
      ],
      entry_points={
          'console_scripts': [
              'td = termdict.main:main',
          ]
      },
     )
