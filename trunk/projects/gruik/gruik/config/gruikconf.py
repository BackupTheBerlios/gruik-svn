#!/usr/bin/env python2.4
# -*- encoding: latin1 -*-

# $Id$

import time
import os
import scapy
from gruik.tools.config_manager import ConfigManager
from gruik.tools.log_manager import logger

#possible_layers = [item[1] for item in lso()]

## - - - - - - - - - - - -
## Application settings:
## - - - - - - - - - - - -

GLOBAL_CONFIG_FILE = '/etc/gruik/gruik.conf'
GRUIK_CONFIG_FILE_SPECS = '/etc/gruik/gruik.conf.specs'
USER_CONFIG_FILE = os.getenv('HOME') + os.sep  + '.gruikrc'
CONFIG_FILENAMES = [GLOBAL_CONFIG_FILE, USER_CONFIG_FILE]

ConfigObjOptions = dict(raise_errors=True,
                        list_values=True,
                        create_empty=False,
                        file_error=False,
                        interpolation=True,
                        stringify=True,
                        indent_type=' ',
                        configspec=GRUIK_CONFIG_FILE_SPECS)

GruikConf = ConfigManager(CONFIG_FILENAMES, ConfigObjOptions, default_namespace='SETTINGS')

## - - - - - -
## protocols:
## - - - - - -

ConfigObjOptions = dict(raise_errors=True,
                        list_values=True,
                        create_empty=False,
                        file_error=True,
                        #file_error=False,
                        interpolation=True,
                        stringify=True,
                        indent_type=' ',
                        configspec=None)

PROTOCOLS_CONFIG_FILE = '/etc/gruik/protocols.conf'
ProtocolsConf = ConfigManager([PROTOCOLS_CONFIG_FILE], ConfigObjOptions, default_namespace='STANDARD')

standard_layers = []
#for v in ProtocolsConf['STANDARD'].values():
for v in ProtocolsConf.dico['STANDARD'].values():
    standard_layers.extend(v)

#all_layers = []
#for v in ProtocolsConf['NON_STANDARD'].values():
#    all_layers.extend(v)

## - - - - -
## Logging
## - - - - -

LOGGING_CONFIG_FILE = '/etc/gruik/logging.conf'
# XXX LogConf


## - - - - - - - - - - -
## Template Dictionnary
## - - - - - - - - - - -

class TemplateDict(object):
    def __init__(self, packet=None):
        self.packet = packet

    def color_dict(self):
        __name__ = 'color'
        return dict(normal ="\033[0m",
                    black  ="\033[30m",
                    red    ="\033[31m",
                    green  ="\033[32m",
                    yellow ="\033[33m",
                    blue   ="\033[34m",
                    purple ="\033[35m",
                    magenta="\033[35m",
                    cyan   ="\033[36m",
                    grey   ="\033[37m",
                    bold   ="\033[1m",
                    uline  ="\033[4m",
                    blink  ="\033[5m",
                    invert ="\033[7m")

    def time_dict(self, timestr):
        __name__ = 'time'
        return dict(now=str(time.strftime(timestr, time.localtime())))

    def packet_dict(self):
        __name__ = 'packet'
        notfound = '??'
        gpa = get_packet_attr
        d = {}
        d['flags' ] = get_flags(self.packet)
        d['sport' ] = gpa(self.packet, 'sport') or notfound
        d['dport' ] = gpa(self.packet, 'dport') or notfound
        d['src'   ] = gpa(self.packet, 'src') or gpa(self.packet, 'psrc') or notfound
        d['dst'   ] = gpa(self.packet, 'dst') or gpa(self.packet, 'pdst') or notfound
        d['macsrc'] = self.packet.getlayer(scapy.Ether).src or gpa(self.packet, 'hwsrc') or notfound
        d['macdst'] = self.packet.getlayer(scapy.Ether).dst or gpa(self.packet, 'hwdst') or notfound
        d['layers'] = str(layers(self.packet)) or notfound
        return d

    def theme_dict(self):
        __name__ = 'theme'
        d = {}
        ns = 'COLORS'
        GruikConf.setNamespace(ns)
        for key in GruikConf.dico[ns].keys():
            d[key] = '$%s$%s$normal' % (GruikConf.getValue(key), key)
        return d

## - - - - - -
## Utilities
## - - - - - -

def layers(x, ignore=['Ethernet'], output='names', limit=5):
    xlayers = []
    for l in standard_layers:
        y = x.getlayer(getattr(scapy, l))
        if y and (y.name not in ignore):
            if len(xlayers) == limit:
                return xlayers
            if output == 'objects':
                xlayers.append(y)
            elif output == 'names':
                xlayers.append(y.name)
            else:
                raise Exception, 'incorrect output type'
    return xlayers

def get_flags(packet):
    flags = get_packet_attr(packet, 'flags') or 0
    return scapy.TCPflags2str(int(flags))

def get_packet_attr(packet, attrname, ignore=['Ethernet']):
    attr = ''
    for l in layers(packet, ignore, output='objects'):
        if hasattr(l, attrname):
            return getattr(packet.getlayer(l.__class__), attrname)
    return attr

