#/usr/bin/env python
# -*- encoding: utf-8 -*-

import gtk
from confpacupdate import ConfPacupdate

class PreferencesWindows:

    conf_options = [['update_interval', '60'],
                    ['notification_delay', '10']]

    def destroy(self, widget):
        '''
	Destroy a window
	'''
        self.window.destroy()

    def create_frame(self, parent, label):
        '''
	Create a frame window
	'''

        # Add bold to label
        bold_label = gtk.Label("<b> " + label + " </b>")
        bold_label.set_use_markup(True) # Enable Pango markup
        bold_label.show()

        # Set the label and frame
        frame = gtk.Frame()
        frame.set_label_widget(bold_label)
        frame.set_shadow_type(gtk.SHADOW_NONE)
        frame.show()

        box = gtk.VBox(False, 0);
        box.set_border_width(6)
        box.show();

        frame.add(box)
        parent.pack_start(frame, False, False, 0)

        return box

    def spinbutton_callback(self, widget, key):
        '''
		Sets spinbutton callback
		'''

        self.conf_options[key][1] = str(int(widget.get_value()))


    def spinnbutton(self, parent, label, default, key):
        '''
		Create a spinnbutton
		'''

        # Creating a horizontal box
        box = gtk.HBox(False, 12);
        parent.pack_start(box)
        box.show();

        # Adding label
        label = gtk.Label(label)
        box.pack_start(label, False, False, 0)
        label.show()

        # Make some ajustments like default value
        # max value, increase value etc
        adjustment = gtk.Adjustment(default, 1, 3600, 1, 10)
        spinbutton = gtk.SpinButton(adjustment)
        spinbutton.set_numeric(True)
        spinbutton.set_update_policy(gtk.UPDATE_IF_VALID)
        spinbutton.connect("value-changed", self.spinbutton_callback, key)
        box.pack_end(spinbutton, False, False, 0)
        spinbutton.show()

        return box

    def __init__(self):

        # main window
        self.window = gtk.Window(gtk.WINDOW_TOPLEVEL)
        self.window.set_title(_('Pacupdate Preferences'))
        self.window.set_resizable(False)
        self.window.set_position(gtk.WIN_POS_CENTER)

        # Close window
        self.window.connect("destroy", self.destroy)

        # main container in window
        self.box_main = gtk.VBox(False, 12)
        self.box_main.set_border_width(12)
        self.window.add(self.box_main)
        self.box_main.show()

        # Updates box and options
        self.updates_frame = self.create_frame(self.box_main, _('Update options'))
        self.updates_hidebox = gtk.VBox(False, 6)
        self.updates_frame.pack_start(self.updates_hidebox)
        self.updates_hidebox.show()

        # Get update_interval value using ConfPacupdate.readConf
        # Set spinnbutton value
        self.spinnbutton(self.updates_hidebox, _('Check for updates every (minutes)'), int(ConfPacupdate().readConf().get('global', self.conf_options[0][0])), 0)
        self.spinnbutton(self.updates_hidebox, _('Show notification for (in seconds)'), int(ConfPacupdate().readConf().get('global', self.conf_options[1][0])), 1)

        # Horizontal button box
        self.box_buttons = gtk.HButtonBox()
        self.box_buttons.set_layout(gtk.BUTTONBOX_END)
        self.box_buttons.set_spacing(6)
        self.box_main.pack_end(self.box_buttons, False, False, 0)
        self.box_buttons.show()

        # Cancel Button
        self.button_cancel = gtk.Button(stock=gtk.STOCK_CANCEL)
        self.button_cancel.connect("clicked", self.destroy)
        self.box_buttons.pack_end(self.button_cancel, False, False, 0)
        self.button_cancel.show()

        # OK Button
        self.button_apply = gtk.Button(stock=gtk.STOCK_OK)
        self.button_apply.connect("clicked", self.apply_button)
        self.box_buttons.pack_start(self.button_apply, False, False, 0)
        self.button_apply.show()
        self.button_apply.grab_focus()

        # Show the preferences window
        self.window.show()

    def apply_button(self,widget):
        try:
            ConfPacupdate().writeConf(self.conf_options[0][1],self.conf_options[1][1])
        except:
            print _('Oops. Something bad happened. Run and save your life.')

        self.window.destroy()

if __name__ == '__main__':
    PreferencesWindows()
    #gtk.main()


