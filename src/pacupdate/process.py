#!/usr/bin/env python
# -*- encoding: utf-8 -*-

from os import fork, system, waitpid, path, WNOHANG
import gtk
import sys
from subprocess import Popen, PIPE

class ProcessUpdate():

    def db_islocked(self):
        """Check if we already have a db lock"""		
        path_db = '/var/lib/pacman/db.lck'
        if path.isfile(path_db):
            return True

    def run_background(self,cmd):
        """ run_background(cmd) -> exit_status
            Runs cmd in background, processing gtk events in the meanwhile. The
            function returns only when the command is done.
        """

        pid = fork()
        if pid == 0:
            # Here we are in the child process.
            # Exit returning the command exit status.
            sys.exit(system(cmd))

        # Here we are in the parent process. Wait the child process to exit,
        # processing gtk events in the meanwhile.
        while True:
            # Process gtk events.
            while gtk.events_pending(): gtk.main_iteration()
            # Check if the child process (pid) is still running.
            (wpid, wstatus) = waitpid(pid, WNOHANG)
            if wpid == pid:
                # Child process is done. Return its exit status.
                return wstatus
