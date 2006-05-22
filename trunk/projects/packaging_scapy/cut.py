#!/usr/bin/python

import sys, os
import re


class ScapyDissector:
    def __init__(self, filename, docdir, libdir):
        self.filename = filename
        self.docdir = docdir
        self.libdir = libdir
        self.scapylines = self._readScapy()
        self.bounds = {}

    def _readScapy(self):
        fd = open(self.filename)
        lines = fd.readlines()
        fd.close()
        return lines

    def process(self):
        self._getBounds()
        self._writeFiles()

    def _getBounds(self):
        self.getLicenseBounds()
        self.getChangeLogBounds()
        self.getTodoBounds()

    def getLicenseBounds(self):
        c = 0
        lines = self.scapylines
        start, end = -1, -1
        for line in lines:
            c += 1
            ln = c-1
            if lines[ln].startswith('##########################################################') \
               and lines[ln+1].startswith('##'):
               start = ln
            if lines[ln].startswith('##########################################################') \
               and lines[ln-1].startswith('##'):
               end = ln+1
        if start and end:
            self.bounds['LICENSE'] = dict(start=start, end=end)
        else:
            msg = """LICENSE section not found"""
            err = DissectError(msg)
            raise err
        return (start, end)

    def getChangeLogBounds(self):
        c = 0
        lines = self.scapylines
        start, end = -1, -1
        for line in lines:
            c += 1
            ln = c-1
            if lines[ln].startswith('#') \
               and lines[ln+1].startswith('# $Log: scapy.py,v $') \
               and re.search('# Revision', lines[ln+2]):
               start = ln
            if lines[ln][0:2] == '#\n' \
               and lines[ln+1][0:2] == '#\n' \
               and lines[ln+2] == '\n':
               end = ln+2
            if start and end:
                self.bounds['ChangeLog'] = dict(start=start, end=end)
            else:
                msg = 'ChangeLog section not found\n'
                err = DissectError(msg)
                raise err
        return (start, end)

    def getTodoBounds(self):
        c = 0
        lines = self.scapylines
        start, end = -1, -1
        for line in lines:
            c += 1
            ln = c-1
            if lines[ln].startswith('##########[XXX]#=-') \
               and lines[ln+1].startswith('##'):
               start = ln
            if lines[ln].startswith('##########[XXX]#=-') \
               and lines[ln-1].startswith('##'):
               end = ln+1
            if start and end:
                self.bounds['TODO'] = dict(start=start, end=end)
            else:
                msg = 'TODO section not found\n'
                err = DissectError(msg)
                raise err
        return (start, end)

    def _writeFiles(self):
        self.writeLicenseFile()
        self.writeChangeLogFile()
        self.writeTodoFile()
        self.writeScapyFile()
        print """No errors, so I think it's done"""

    def writeLicenseFile(self):
        bounds = self.bounds['LICENSE']
        if bounds:
            start, end = bounds['start'], bounds['end']
            filepath = os.path.join(self.docdir + os.sep + 'LICENSE')
            fd = open(filepath, 'w')
            fd.writelines(self.scapylines[start:end])
            fd.close()
        else:
            msg = 'Error: LICENSE bounds not found\n'
            err = DissectError(msg)
            raise err

    def writeChangeLogFile(self):
        bounds = self.bounds.get('ChangeLog', None)
        if bounds:
            start, end = bounds.get('start', 0), bounds.get('end', 0)
            filepath = os.path.join(self.docdir + os.sep + 'ChangeLog')
            fd = open(filepath, 'w')
            fd.writelines(self.scapylines[start:end])
            fd.close()
        else:
            msg = 'Error: ChangeLog bounds not found\n'
            err = DissectError(msg)
            raise err

    def writeTodoFile(self):
        bounds = self.bounds.get('TODO', None)
        if bounds:
            start, end = bounds.get('start', 0), bounds.get('end', 0)
            filepath = os.path.join(self.docdir + os.sep + 'TODO')
            fd = open(filepath, 'w')
            fd.writelines(self.scapylines[start:end])
            fd.close()
        else:
            msg = 'Error: TODO bounds not found\n'
            err = DissectError(msg)
            raise err

    def writeScapyFile(self):
        license_bounds = self.bounds.get('LICENSE', None)
        changelog_bounds = self.bounds.get('ChangeLog', None)
        todo_bounds = self.bounds.get('TODO', None)
        if license_bounds and changelog_bounds and todo_bounds:
            filepath= os.path.join(self.libdir + os.sep + 'scapy.py')
            fd = open(filepath, 'w')
            newscapylines = self.scapylines[0:license_bounds['start']-1] + \
                            self.scapylines[changelog_bounds['end']:todo_bounds['start']-1] + \
                            self.scapylines[todo_bounds['end']:]
            newscapylines.append('\n')
            fd.writelines(newscapylines)
            fd.close()
        else:
            msg = """Error in file bounds: %s""" % self.bounds
            err = DissectError(msg)
            raise err


class DissectError(StandardError):
    def __init__(self, message, dico=None):
        self.message = message
        self.dico = dico

    def __str__(self):
        if self.dico is not None:
            txt = self.message % self.dico
        else:
            txt = self.message
        return txt


def _main():
    try:
        filename = sys.argv[1]
    except IndexError:
        sys.exit('Error: the first argument must be the path to scapy source file\n')
    try:
        docdir = sys.argv[2]
    except IndexError:
        sys.exit('Error: the second argument must be the path to doc directory\n')
    try:
        libdir = sys.argv[3]
    except IndexError:
        sys.exit('Error: the third argument must be the path to lib directory\n')

    scapy_dissect = ScapyDissector(filename, docdir, libdir)
    scapy_dissect.process()


if __name__ == '__main__':
    _main()

