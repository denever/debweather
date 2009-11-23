#!/usr/bin/env python
# -*- Python -*-
###########################################################################
#                        Python Debian Weather                            #
#                        --------------------                             #
#  copyright         (C) 2008  Giuseppe "denever" Martino                 #
#  email                : denever@users.sf.net                            #
###########################################################################
###########################################################################
#                                                                         #
#   This program is free software; you can redistribute it and/or modify  #
#   it under the terms of the GNU General Public License as published by  #
#   the Free Software Foundation; either version 2 of the License, or     #
#   (at your option) any later version.                                   #
#                                                                         #
#  This program is distributed in the hope that it will be useful,        #
#  but WITHOUT ANY WARRANTY; without even the implied warranty of         #
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the          #
#  GNU General Public License for more details.                           #
#                                                                         #
#  You should have received a copy of the GNU General Public License      #
#  along with this program; if not, write to the Free Software            #
#  Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA#
#                                                                         #
###########################################################################

import pygtk
pygtk.require('2.0')

import gtk
import gnomeapplet
import gobject

class WeatherIcon(gtk.Label):
    def set_clear(self):
        self.set_label("Debian Weather: Clear")

    def set_few_clouds(self):
        self.set_label("Debian Weather: Few clouds")

    def set_overcast(self):
        self.set_label("Debian Weather: Overcast")

    def set_shower(self):
        self.set_label("Debian Weather: Shower scattered")

    def set_storm(self):
        self.set_label("Debian Weather: Storm")

def background_show(applet):
    print "background: ", applet.get_background()

def sample_factory(applet, iid):
    print "Creating new applet instance"
    weathericon = WeatherIcon()
    weathericon.set_storm()
    applet.add(weathericon)
    applet.show_all()
    gobject.timeout_add(1000, background_show, applet)
    return True

print "Starting factory"
gnomeapplet.bonobo_factory("OAFIID:GNOME_PythonAppletSample_Factory",
                           gnomeapplet.Applet.__gtype__,
                           "hello", "0", sample_factory)
print "Factory ended"
