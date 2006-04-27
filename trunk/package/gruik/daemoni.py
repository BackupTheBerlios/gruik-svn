#!/usr/bin/python2.4

# $Id: daemoni.py 25 2005-10-20 20:02:36Z oli $

import sys, os, time
from signal import SIGTERM

class Daemoni(object):
    def __init__(self, stdout='/dev/null', stderr=None, stdin='/dev/null',
                 pidfile=None, startmsg = 'started with pid %s' ):
        self.stdout = stdout
        self.stderr = stderr
        self.stdin = stdin
        self.pidfile = pidfile
        self.startmsg = startmsg
        self.pid = None
        self.action = None

    def startstop(self, action):
        self.action = action
        if self.action in ['start', 'stop', 'restart', 'status']:
            try:
                pf  = file(self.pidfile,'r')
                self.pid = int(pf.read().strip())
                pf.close()
            except IOError:
                self.pid = None
            return self._dispatch()
        else:
            print "usage: %s -d [options] start|stop|restart|status" % sys.argv[0]
            sys.exit(2)

    def _dispatch(self):
        actions = {'start': self._start,
                   'stop': self._stop_or_restart,
                   'restart': self._stop_or_restart,
                   'status': self._status}
        return actions[self.action]()

    def _start(self):
        if self.pid:
            mess = "Start aborded since pid file '%s' exists.\n"
            sys.stderr.write(mess % self.pidfile)
            sys.exit(1)
        self.__deamonize()
        return

    def _stop_or_restart(self):
        if not self.pid:
            mess = "Could not stop, pid file '%s' missing.\n"
            sys.stderr.write(mess % self.pidfile)
            if self.action == 'stop':
                sys.exit(1)
            self.action = 'start'
            self.pid = None
        else:
           try:
              while 1:
                  os.kill(self.pid, SIGTERM)
                  time.sleep(1)
           except OSError, err:
              err = str(err)
              if err.find("No such process") > 0:
                  os.remove(self.pidfile)
                  if self.action == 'stop':
                      sys.exit(0)
                  self.action = 'start'
                  self.pid = None
              else:
                  print str(err)
                  sys.exit(1)

    def _status(self):
        '''
            State:	S (sleeping)
            VmSize:	   10464 kB
            VmLck:	       0 kB
            VmRSS:	    6352 kB
            VmData:	    4360 kB
            VmStk:	      56 kB
            VmExe:	     852 kB
            VmLib:	    2772 kB
        '''
        try:
            status_file = open('/proc/%s/status' % self.pid)
            lines = status_file.readlines()
        finally:
            status_file.close()
        for line in lines:
            if line.startswith('State:'):
                print line

    def __deamonize(self):
        '''
            This forks the current process into a daemon.
            The stdin, stdout, and stderr arguments are file names that
            will be opened and be used to replace the standard file descriptors
            in sys.stdin, sys.stdout, and sys.stderr.
            These arguments are optional and default to /dev/null.
            Note that stderr is opened unbuffered, so
            if it shares a file with stdout then interleaved output
            may not appear in the order that you expect.
        '''
        # Do first fork.
        try:
            pid = os.fork()
            if pid > 0:
                sys.exit(0) # Exit first parent.
        except OSError, e:
            sys.stderr.write("fork #1 failed: (%d) %s\n" % (e.errno, e.strerror))
            sys.exit(1)

        # Decouple from parent environment.
        os.chdir("/")
        os.umask(0)
        os.setsid()

        # Do second fork.
        try:
            pid = os.fork()
            if pid > 0:
                sys.exit(0) # Exit second parent.
        except OSError, e:
            sys.stderr.write("fork #2 failed: (%d) %s\n" % (e.errno, e.strerror))
            sys.exit(1)

        # Open file descriptors and print start message
        if not self.stderr:
            self.stderr = self.stdout
        si = file(self.stdin, 'r')
        so = file(self.stdout, 'a+')
        se = file(self.stderr, 'a+', 0)
        pid = str(os.getpid())
        sys.stderr.write("\n%s\n" % self.startmsg % pid)
        sys.stderr.flush()
        if self.pidfile:
            file(self.pidfile,'w+').write("%s\n" % pid)

        # Redirect standard file descriptors.
        os.dup2(si.fileno(), sys.stdin.fileno())
        os.dup2(so.fileno(), sys.stdout.fileno())
        os.dup2(se.fileno(), sys.stderr.fileno())


