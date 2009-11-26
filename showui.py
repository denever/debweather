#!/usr/bin/python

import pygtk
import gtk

gui = gtk.Builder()
gui.add_from_file('./prefbox.glade')
prefs = gui.get_object('prefs')
prefs.show_all()
gtk.main()

