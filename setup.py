# -*- coding: utf-8 -*-
##############################################################################
#
# Copyright © 2014 OnlineGroups.net and Contributors.
# All Rights Reserved.
#
# This software is subject to the provisions of the Zope Public License,
# Version 2.1 (ZPL).  A copy of the ZPL should accompany this distribution.
# THIS SOFTWARE IS PROVIDED "AS IS" AND ANY AND ALL EXPRESS OR IMPLIED
# WARRANTIES ARE DISCLAIMED, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF TITLE, MERCHANTABILITY, AGAINST INFRINGEMENT, AND FITNESS
# FOR A PARTICULAR PURPOSE.
#
##############################################################################
from setuptools import setup, find_packages
import codecs
import os
from version import get_version

with codecs.open('README.rst', encoding='utf-8') as f:
    long_description = f.read()
with codecs.open(os.path.join("docs", "HISTORY.rst"),
                 encoding='utf-8') as f:
    long_description += '\n' + f.read()

version = get_version()
setup(name='Products.GSRedirect',
      version=version,
      description="",
      long_description=long_description,
      classifiers=[
        'Development Status :: 5 - Production/Stable',
        "Environment :: Web Environment",
        "Framework :: Zope2",
        "Intended Audience :: Developers",
        'License :: OSI Approved :: Zope Public License',
        "Natural Language :: English",
        "Operating System :: POSIX :: Linux",
        "Programming Language :: Python",
        "Topic :: Software Development :: Libraries :: Python Modules",
      ],
      keywords='post, topic, image, file, redirect',
      author='Michael JasonSmith',
      author_email='mpj17@onlinegroups.net',
      url='https://github.com/groupserver/Products.GSRedirect/',
      license='ZPL 2.1',
      packages=find_packages(exclude=['ez_setup']),
      namespace_packages=['Products'],
      include_package_data=True,
      zip_safe=False,
      install_requires=[
          'setuptools',
          'Products.XWFFileLibrary2',
          'Products.XWFMailingListManager',
          'zope.browserpage',
          'zope.cachedescriptors',
          'zope.component',
          'zope.interface',
          'zope.publisher',
      ],
      entry_points="""
      # -*- Entry points: -*-
      """,
      )
