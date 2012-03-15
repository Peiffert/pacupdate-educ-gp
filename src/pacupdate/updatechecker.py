#!/usr/bin/env python
# -*- encoding: utf-8 -*-

from os import popen
from re import compile, split, sub
from process import ProcessUpdate
from pynotify import URGENCY_NORMAL, URGENCY_CRITICAL, URGENCY_LOW 
from confpacupdate import ConfPacupdate
import gtk
import i18n

class UpdateChecker:
    
    def cut_packages(self, targets_list, targets):
        list=[]
        list.append(targets)
        for index,item in enumerate(targets_list):
            pkg = split('-\d',targets_list[index])[0]
            list.append(pkg)
        return list

    def sync_db(self):
        if not ProcessUpdate().db_islocked():
            print _('Syncing databases')
            try:
                if ProcessUpdate().run_background('sudo pacman -Sy') == 0:
                    return True
            except KeyboardInterrupt:
                return False
        else:
            print _('Pacman is already running!')
            return False

    def get_updates(self):
        print _("Checking updates")
        command = popen('LC_ALL="C" pacman -Qu | egrep -vi "^(Checking|warning|Remove|Total)"').read().strip()
        if compile('Targets \(.*\):').match(command,0):
            targets_list = sub('Targets \(.*\):','',command).split()
            targets = compile('\(.*\)').findall(command)
            return self.cut_packages(targets_list, targets[0])
        else:
            return None
        
    def get_totaldownload(self):
        print _('Getting total download size')
        command = popen('LC_ALL="C" pacman -Qu | egrep -i ^"Total Download Size"').read().strip()
        return  command.split(':')[1].strip()
