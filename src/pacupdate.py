#!/usr/bin/env python
# -*- encoding: utf-8 -*-

from pacupdate.tray import PacupdateTrayIcon
from pacupdate.confpacupdate import ConfPacupdate
from pacupdate.updatechecker import UpdateChecker
from gtk import main
from gobject import timeout_add

 intervalUpdate = 60000
def call_updates(data=None):
    '''
    Call the update method
    '''
    
    pacupdate.on_updates(PacupdateTrayIcon)
    return True

# Create a instance of PacupdateTrayIcon
pacupdate = PacupdateTrayIcon()

# Create the trayicon
pacupdate.create_tray()

# Get the time of interval
update_time = int(ConfPacupdate().readConf().get('global', 'update_interval')) * intervalUpdate

# Run updates periodically
call = timeout_add(int(update_time), call_updates, pacupdate)

try:
    main()
except KeyboardInterrupt:
    pass
