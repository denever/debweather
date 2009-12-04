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

import pygtk
pygtk.require('2.0')
import gtk
import gconf
import logging
import popen2
from debweatherlib import Paths
from debweatherlib import PreferencesBox

logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s %(levelname)-8s %(message)s',
                    datefmt='%a, %d %b %Y %H:%M:%S',
                    filename='/tmp/showui.log',
                    filemode='w')

def on_new_preferences(widget, distro, arch):
    print widget
    print 'New preferences %s %s' % (distro, arch)

def main():
    paths = Paths(__file__)
    conf_client = gconf.client_get_default()    
    distro = str()
    arch = str()
    if not conf_client.dir_exists('/apps/debian-weather-applet'):
        debian_version = open('/etc/debian_version','r').readline().strip()
        print debian_version
        stdout, stdin = popen2.popen2('dpkg --print-architecture')
        arch = stdout.readline().strip()
        print arch
        distro = 'unstable'
    else:
        distro = conf_client.get_string('/apps/debian-weather-applet/distro')
        arch = conf_client.get_string('/apps/debian-weather-applet/arch')

    pb = PreferencesBox(paths, distro, arch)
    pb.show()
    pb.connect('new-preferences', on_new_preferences)
    gtk.main()

if __name__ == "__main__":
    main()
