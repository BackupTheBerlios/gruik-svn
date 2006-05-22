#!/usr/bin/env python
# -*- coding: iso-8859-1 -*-

# $Id: setup.py 30 2005-10-30 07:24:38Z oli $

import os, sys
from setuptools import setup, find_packages

sys.path.insert(0, 'package/lib')
from scapy import VERSION

PACKAGE_NAME = 'scapy'

DESCRIPTION="""Packet manipulation tool, packet generator, network scanner, packet sniffer, and much more."""
LONG_DESCRIPTION="""Powerful interactive packet... manipulation tool, packet generator, \
network... scanner, network discovery tool, and packet... sniffer."""

def find_data_files():
    files = [
             ('/usr/local/share/doc/scapy/', ['package/doc/LICENSE']),
             ('/usr/local/share/doc/scapy/', ['package/doc/ChangeLog']),
             ('/usr/local/share/doc/scapy/', ['package/doc/TODO']),
             ('/usr/local/bin/', ['package/usr/bin/iscapy'])
            ]
    if os.path.exists('package/doc/scapy.info.gz'):
        files.append( ('/usr/local/info/', ['package/doc/scapy.info.gz']) )
    if os.path.exists('package/doc/scapy.1.gz'):
        files.append( ('/usr/local/man/man1', ['package/doc/scapy.1.gz']) )
    return files


setup(name=PACKAGE_NAME,
      version=VERSION,
      license = """GNU General Public License (GPL)""",
      platforms = ['POSIX'],
      description = DESCRIPTION,
      long_description = LONG_DESCRIPTION,
      url = "http://www.secdev.org/projects/scapy/",
      download_url = "http://www.secdev.org/projects/scapy/files/scapy.py",
      author = "Philippe Biondi",
      author_email = "phil@secdev.org",
      classifiers = ["""Development Status :: 4 - Beta""",
                     """Environment :: Console""",
                     """Intended Audience :: Developers""",
                     """Intended Audience :: Education""",
                     """Intended Audience :: End Users/Desktop""",
                     """Intended Audience :: Information Technology""",
                     """Intended Audience :: Other Audience""",
                     """Intended Audience :: Science/Research""",
                     """Intended Audience :: System Administrators""",
                     """License :: OSI Approved :: GNU General Public License (GPL)""",
                     """Natural Language :: English""",
                     """Operating System :: POSIX""",
                     """Programming Language :: Python""",
                     """Topic :: Education :: Testing""",
                     """Topic :: Internet""",
                     """Topic :: Scientific/Engineering :: Interface Engine/Protocol Translator""",
                     """Topic :: Security""",
                     """Topic :: Software Development :: Libraries :: Python Modules""",
                     """Topic :: Software Development :: Testing""",
                     """Topic :: Software Development :: Testing :: Traffic Generation""",
                     """Topic :: System""",
                     """Topic :: System :: Networking""",
                     """Topic :: System :: Networking :: Firewalls""",
                     """Topic :: System :: Networking :: Monitoring"""],
      package_dir = {'':'package/lib'},
      py_modules = ['scapy'],
      zip_safe=True,
      data_files = find_data_files()
      )


