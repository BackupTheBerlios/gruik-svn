#!/usr/bin/env python
# -*- coding: iso-8859-1 -*-

# $Id: $

import os, sys
from setuptools import setup, find_packages

sys.path.append('package/gruik')

from version import __version__ as VERSION

PACKAGE_NAME = 'gruik'

DESCRIPTION="""Packet sniffer."""
LONG_DESCRIPTION="""Console Packet Sniffer with configurable output colorizing and """

setup(name=PACKAGE_NAME,
      version=VERSION,
      license = """GNU General Public License (GPL)""",
      platforms = ['POSIX'],
      description = DESCRIPTION,
      long_description = LONG_DESCRIPTION,
      url = "file://localhost",
      download_url = "file://localhost",
      author = "Olivier laurent",
      author_email = "olilau@gmail.com",
      classifiers = ["""Development Status :: 4 - Beta""",
                     """Environment :: Console""",
                     """Intended Audience :: Information Technology""",
                     """Intended Audience :: System Administrators""",
                     """License :: OSI Approved :: GNU General Public License (GPL)""",
                     """Natural Language :: English""",
                     """Operating System :: POSIX""",
                     """Programming Language :: Python""",
                     """Topic :: Internet""",
                     """Topic :: Security""",
                     """Topic :: System""",
                     """Topic :: System :: Networking""",
                     """Topic :: System :: Networking :: Firewalls""",
                     """Topic :: System :: Networking :: Monitoring"""],
      #install_requires = 'scapy>=1.0.1',
      #install_requires = 'configobj>=4.0.0',
      package_dir = {'':'package'},
      packages = find_packages('package'),
      data_files = [
                    ('/usr/local/share/doc/gruik/', ['package/doc/LICENSE',
                                                     'package/doc/TODO']),
                    ('/usr/local/bin/', ['package/usr/bin/gruik']),
                    ('/etc/gruik/', ['package/etc/gruik/gruik.conf',
                                     'package/etc/gruik/gruik.conf.specs',
                                     'package/etc/gruik/protocols.conf',
                                     'package/etc/gruik/logging.conf']),
                    ('/var/log/gruik/', ['package/var/log/gruik/app.log',
                                         'package/var/log/gruik/error.log',
                                         'package/var/log/gruik/debug.log']),
                    ('/usr/local/share/zsh/site-functions/', ['package/usr/share/zsh/site-functions/_gruik']),
                    ('/usr/local/man/man1', ['package/doc/gruik.1.gz']),
                    ('/usr/local/info/', ['package/doc/gruik.info.gz'])
                   ],
      )


