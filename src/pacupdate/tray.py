#!/usr/bin/env python
# -*- encoding: utf-8 -*-

from os import path
import pygtk
pygtk.require('2.0')
from gui import PreferencesWindows
from updatechecker import UpdateChecker
from confpacupdate import ConfPacupdate
import gtk
import i18n
try:
    from pynotify import init, Notification, URGENCY_LOW, URGENCY_CRITICAL, URGENCY_NORMAL
except:
    print _('Install python-notify to use pacupdate.')


class PacupdateTrayIcon(gtk.StatusIcon):
    
    '''
    Create a trayicon of pacupdate
    '''

    data_dir = '/usr/share/pacupdate'
    pacupdate_tray_icon = data_dir + '/img/pacupdate-pack.png'
    pacupdate_tray_icon_alert = data_dir + '/img/pacupdate-alert.png'

    def check_data_dir(self):
        '''
	Check if pacupdate data directory exists. It is used to see if pacupdate is already
        installed or not.
	'''
        
        if path.exists('/usr/share/pacupdate'):
            return True

    def create_tray(self):
        
        gtk.StatusIcon.__init__(self)

        if not self.check_data_dir():
            print _('pacupdate did not found images directory (perhaps pacupdate is not installed?).')
            print _('Using current directory.')
            
            self.data_dir = '.'
            self.pacupdate_tray_icon = self.data_dir + '/img/pacupdate-pack.png'
            self.pacupdate_tray_icon_alert = self.data_dir + '/img/pacupdate-alert.png'

        menu = '''
             <ui>
             <menubar name="Menubar">
             <menu action="Menu">
             <menuitem action="Check for updates"/>
             <menuitem action="Preferences"/>
             <menuitem action="About"/>
             <separator/>
             <menuitem action="Quit"/>
             </menu>
             </menubar>
             </ui>
             '''
        
        actions = [
            ('Menu',  None, 'Menu'),
            ('Check for updates', gtk.STOCK_FIND, _('Check for updates'), None, 'Check updates for your system', self.on_updates),
            ('Preferences', gtk.STOCK_PREFERENCES, _('Preferences'), None, 'Change pacupdate preferences', self.on_preferences),
            ('About', gtk.STOCK_ABOUT, _('About'), None, 'About pacupdate', self.on_about),
            ('Quit', gtk.STOCK_QUIT, _('Quit'), None, 'Exit pacupdate', self.on_quit)]

        action_groups = gtk.ActionGroup('Actions')
        action_groups.add_actions(actions)

        self.manager = gtk.UIManager()
        self.manager.insert_action_group(action_groups, 0)
        self.manager.add_ui_from_string(menu)
        self.menu = self.manager.get_widget('/Menubar/Menu/About').props.parent
        
        try:
            self.set_from_file(self.pacupdate_tray_icon)
            self.set_tooltip(_('Pacupdate - Managing your Arch Linux Updates'))
            self.set_visible(True)
            self.connect('popup-menu', self.on_popup_menu)
            self.connect('activate', self.on_updates, False)
            
        except:
            print _('Your system is not able to show pacupdate tray icon.')
            self.on_quit()

    def on_popup_menu(self, status, button, time):
        self.menu.popup(None, None, None, button, time)

    def check_updates(self, sync):
        '''
        Get (and return) all updates available
        
        @sync: used to sync pacman's DB or not
        
        '''

        # Syncing data bases and getting updates
        try:
            self.set_blinking(True)
            self.set_tooltip(_('Syncing databases...'))
            if sync:
                if UpdateChecker().sync_db() == False:
                    self.set_blinking(False)
                    return False
            updates = UpdateChecker().get_updates()
            self.set_blinking(False)
            self.set_tooltip(_('Pacupdate - Managing your Arch Linux Updates'))
            return updates
        
        except KeyboardInterrupt:
            print _('Bye Bye ... :)')
            pass
        
    def show_updates(self, notification, action):
        assert action == 'show_updates'        
        notification.close()    
        self.on_updates(False,True)
    
    def create_notification(self, title, updates, urgency, icon, updates_available):
        '''
        Create a notification message.
        
        @title: Title of the notification
        @updates: Update message (packages)
        @urgency: Used to set the notification urgency (notice, important and so on)
        @icon: Set the notification's icon
        @updates_available: Used to decide which button should be add to the notification
        
        '''

        # Setting notification_delay
        timeout = int(ConfPacupdate().readConf().get('global', 'notification_delay')) * 1000

        if not init( "pacupdate"):
            print _('Failed to init pynotify. Please, verify if python-notify is installed.')

        else:            
            self.notification = Notification(title, updates.strip() + '\n')
            self.notification.set_urgency(urgency)
            self.notification.set_timeout(timeout)
            self.notification.set_icon_from_pixbuf(icon)
            self.notification.attach_to_status_icon(self)            
            
            # Just show a "check for updates button" in the notification if
            # there are updates available
            if updates_available:
                self.notification.add_action('show_updates', 'Show full updates list',self.show_updates)
            
            if not self.notification.show():
                print _('Failed to show notification.')


    def on_updates(self, sync=True,showFull=False):
        '''
        Setup messages, icon, urgency and title for the notification.
        They can different depending if there is a update available or not
        
        @sync: set True to sync pacupdate's DB
        @showFull: Used to show full update list or not. By default shows just 10 packages
        
        '''

        packages_list = self.check_updates(sync)
        if packages_list == False:
            return None

        if packages_list == None:

            title = _('Your system is up to date')
            message = _('There are no updates available for your system or you did not run "Check for updates" yet.')
            urgency = URGENCY_NORMAL
            icon = gtk.Button().render_icon(gtk.STOCK_DIALOG_INFO, gtk.ICON_SIZE_DIALOG)
            self.set_from_file(self.pacupdate_tray_icon)
            updates_available = False

        else:
            
            message = ''
            if showFull == False:
                for package in packages_list[1:11]:
                    message = message + ' ' + package
            
            else:
                for package in packages_list[1:]:
                    message = message + ' ' + package
                
            message = message + '\n\n' + '<b>Total download size:</b> ' + UpdateChecker().get_totaldownload()

            title = 'pacupdate :: ' + _('%s Update(s) available') % packages_list[0]
            icon = gtk.Button().render_icon(gtk.STOCK_DIALOG_WARNING, gtk.ICON_SIZE_DIALOG)
            urgency = URGENCY_CRITICAL
            self.set_from_file(self.pacupdate_tray_icon_alert)
            updates_available = True

        # Creates the notification
        self.create_notification(title, message.strip(), urgency, icon, updates_available)

    def on_preferences(self, data):
        '''
        Method to call the preferences window.
        '''
        PreferencesWindows()
        
    def on_about(self, data):
        '''
        Method to create about window.
        '''
        
        dialog = gtk.AboutDialog()
        dialog.set_name('pacupdate')
        dialog.set_version('0.1.1')        
        dialog.set_comments(_('Arch linux (pacman) updates notification'))
        dialog.set_copyright('Copyright - 2008 \n Hugo Doria \n Kessia Pinheiro')
        dialog.set_website('http://code.google.com/p/pacupdate/')
        dialog.set_website_label(_('pacupdate Homepage'))
        dialog.set_authors(["Hugo Doria <hugo@archlinux.org>", 'Kessia Pinheiro <kessia@archlinux-br.org>'])
        dialog.set_license("""pacupdate version 0.1
Copyright (C) 2008  Hugo Doria, hugo@archlinux.org
Copyright (C) 2008  Kessia Pinheiro, kessia@archlinux-br.org

This program is free software; you can redistribute it and/or
modify it under the terms of the GNU General Public License
version 2 as published by the Free Software Foundation;

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied
warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR
PURPOSE. See the GNU General Public License for more
details.

You should have received a copy of the GNU General Public
License along with this program; if not, write to the Free
Software Foundation, Inc., 51 Franklin Street, Fifth Floor,
Boston, MA  02110-1301, USA.
""")
        dialog.set_logo(gtk.gdk.pixbuf_new_from_file(self.pacupdate_tray_icon))
        dialog.run()
        dialog.destroy()

    def on_quit(self, data):
        gtk.main_quit()