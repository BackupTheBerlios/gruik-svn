#!/usr/bin/env python
# -*- encoding: latin1 -*-

# $Id: config_manager.py 30 2005-10-30 07:24:38Z oli $

"""
Module that handle system wide and user config files
"""

__author__ = "Olivier Laurent <olilau@gmail.com>"
__copyright__ = "Copyright (c) 2005 Olivier Laurent"
__license__ = "GPL"
__version__ = "0.5"

from gruik.tools.log_manager import logger

from configobj import ConfigObj
from validate import Validator


class ConfigManager:
    def __init__(self, config_filenames, options={}, default_namespace='DEFAULT'):
        self.warnings = []
        self.errors = []
        self.options = options
        self.config_filenames = self.getFilenames(config_filenames)
        self.configs = self.makeConfig()
        self.dico = self.makeDico()
        self.ns = default_namespace
        self.searchvalue = {}
        self.postInstall()

    def getFilenames(self, filenames):
        """Always returns a list"""
        if hasattr(filenames, '__iter__'):
            filenames = filenames
        else:
            filenames = [filenames]
        return filenames

    def makeConfig(self):
        configs = [ConfigObj(filename, options=self.options) for filename in self.config_filenames]
        if self.options.get('configspec', False):
            from validate import Validator
            val = Validator()
            for cfg in configs:
                test = cfg.validate(val)
                if test == False:
                    self.errors.append(ConfigError("""Error when validating file '%s'""" % cfg.filename))
        return configs

    def makeDico(self):
        dico = {}
        for conf in self.configs:
            dico.update(conf)
        return dico

    def setNamespace(self, ns):
        """Sets the current namespace"""
        self.ns = ns

    def getAllValuesByNamespace(self, ns=None):
        pass

    def getAllValues(self):
        pass

    def find(self, searcharg):
        #searchvalue = {}
        self.searchvalue = {}
        def find_recurse(section, key, searcharg, dup=False):
            if not dup:
                if self.searchvalue.has_key(key):
                    raise ConfigError('''Duplicate value '%s' found''' % key)
            if not self.searchvalue:
                if searcharg == key:
                    self.searchvalue[key] = section[key]
        kw = dict(searcharg=searcharg, dup=False)
        for cfg in self.configs:
            cfg.walk(find_recurse,  call_on_sections=False, **kw)
        return self.searchvalue[kw['searcharg']]

    def getValue(self, varname, ns=''):
        """Return the configured value or the default value"""
        if ns:
            self.ns = ns
        if self.dico.has_key(varname):
            val = self.dico.get(varname)
        else:
            try:
                val = self.dico[self.ns].get(varname)
            except KeyError, msg:
                raise ConfigError("Value '%s' not found" % varname)
        return val

    def postInstall(self):
        if self.errors:
            for err in self.errors:
                print err


class ConfigError(StandardError):
    """Standard Error Class for config file errors."""
    def __init__(self, message, dico=None):
        self.message = message
        self.dico = dico

    def __str__(self):
        if self.dico is not None:
            txt = self.message % self.dico
        else:
            txt = self.message
        return txt


