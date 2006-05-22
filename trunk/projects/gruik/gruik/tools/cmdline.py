#!/usr/bin/env python
# -*- coding: iso-8859-1 -*-

# $Id$

"""
A command line framework. It should ease the creation of command line utility.
"""

__author__ = "Olivier Laurent <olilau@gmail.com>"
__copyright__ = "Copyright (c) 2005 Olivier Laurent"
__license__ = "GPL"
__version__ = "0.2"

from optparse import OptionParser
import sys


class Prog:
    """
    Small object representing the program.
    """
    def __init__(self, version='0.0', usage=''):
        self.version = version
        self.usage = "%prog " + usage


class Option:
    """
    Object representing a single option.
    Parameter(s):
     - short: short option
     - long: long option
     - action: action to be performed by the option parser
     - dest: destination of the option value
     - default: default value
     - help: help message for that option
     - metavar: by default, the name displayed after options that require an
       input is the destination name in uppercase. Metavar can supersede this.
    """
    def __init__(self, short, long, action, dest, metavar=None, default=0, help=''):
        self.short = short
        self.long = long
        self.action = action
        self.dest = dest
        self.metavar = metavar
        self.default = default
        self.help = help
        # XXX beware: 'help' and 'long' are built-ins.


class Args:
    def __init__(self, Prog=Prog(), args_nbr=0, Opts=[]):
        self.parser = OptionParser(version="%prog " + Prog.version,
                                   usage=Prog.usage)
        self.prog = self.parser.get_prog_name()

        self._process_options(Opts)
        (self.options, self.args) = self.parser.parse_args()
        self._verify_args(args_nbr)

    def _verify_args(self, nbr):
        """Verify that the number of arguments is correct."""
        if len(self.args) != nbr:
            self._show_error('incorrect number of arguments')

    def _show_error(self, error_msg):
        """Print the error message and usage"""
        self.parser.error = error_msg
        print self.parser.error
        self.parser.print_help()
        sys.exit(0)

    def _process_options(self, Opts):
        """Add the options to the option parser"""
        for Opt in Opts:
            self.parser.add_option(Opt.short,
                                   Opt.long,
                                   action=Opt.action,
                                   dest=Opt.dest,
                                   metavar=Opt.metavar,
                                   default=Opt.default,
                                   help=Opt.help
                                  )



