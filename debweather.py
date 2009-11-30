#!/usr/bin/env python
# -*- Python -*-
###########################################################################
#                        Python Debian Weather                            #
#                        --------------------                             #
#  copyright         (C) 2008-2009 Giuseppe "denever" Martino             #
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

import logging
logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s %(levelname)-8s %(message)s',
                    datefmt='%a, %d %b %Y %H:%M:%S',
                    filename='/home/denever/applet.log',
                    filemode='w')
import pygtk
pygtk.require('2.0')

import gtk
import gnomeapplet
import gobject
import gconf

from debweatherlib import Paths
from debweatherlib import WeatherIcon

globalpaths = Paths(__file__)

def background_show(applet):
    logging.debug("background: %s" % applet.get_background())

def sample_factory(applet, iid):
    logging.debug("Creating new applet instance")
    conf_client = gconf.client_get_default()    
    distro = str()
    arch = str()
    if not conf_client.dir_exists('/apps/pydebweather'):
       distro = 'unstable'
       arch = 'i386'
    else:
        distro = conf_client.get_string('/apps/pydebweather/distro')
        arch = conf_client.get_string('/apps/pydebweather/arch')

    wi = WeatherIcon(globalpaths, applet.get_size(), distro, arch)
    logging.debug("Created wi")
    applet.add(wi)
    logging.debug("Added wi")
    applet.show_all()
    logging.debug("Showed wi")
    wi.update()
    logging.debug("Updated wi")
    verbs = [('About', wi.show_about),
             ('Prefs', wi.show_prefs),
             ('More', wi.show_more)]
    menu_xml = open(globalpaths.get_in_data_path('menu.xml'),'r').read()
    applet.setup_menu(menu_xml, verbs, None)
    logging.debug("created menu")
    applet.connect('destroy', wi.cleanup)
    applet.connect('button-press-event', wi.on_button_pressed)
    gobject.timeout_add(1000, background_show, applet)
    gobject.timeout_add_seconds(60, wi.update)
    logging.debug("Ending sample factory")
    return True

print "Starting factory"
gnomeapplet.bonobo_factory("OAFIID:GNOME_DebianWeatherApplet_Factory",
                           gnomeapplet.Applet.__gtype__,
                           "hello", "0", sample_factory)
print "Factory ended"
# pydebweather.png in /usr/share/pixmaps
