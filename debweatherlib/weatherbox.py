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
import pygtk
pygtk.require('2.0')

import gtk

class WeatherBox():
    def __init__(self, paths, distro, arch, totpkg, uninstpkg, url):
        self.gui = gtk.Builder()
        self.gui.add_from_file(paths.get_in_data_path('debweather.ui'))
        self.dlg_debweather = self.gui.get_object('dlg_debweather')
        self.lbl_distro = self.gui.get_object('lbl_distro')
        self.lbl_arch = self.gui.get_object('lbl_arch')
        self.lbl_totpkg = self.gui.get_object('lbl_totpkg')
        self.lbl_uninstpkg = self.gui.get_object('lbl_uninstpkg')
        self.lbt_more = self.gui.get_object('lbt_more')
        self.lbl_distro.set_text('Distribution: %s' % distro)
        self.lbl_arch.set_text('Architecture: %s' % arch)
        self.lbl_totpkg.set_text('Total packages: %s' % totpkg)
        self.lbl_uninstpkg.set_text('Uninstallable packages: %s' % uninstpkg)
        self.lbt_more.set_uri(url)

    def show(self):
        self.dlg_debweather.show()
