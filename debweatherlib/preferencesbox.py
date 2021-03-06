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
import gconf
import gobject

class PreferencesBox(gobject.GObject):
    __gsignals__ = {
    'new-preferences':(gobject.SIGNAL_RUN_LAST, gobject.TYPE_NONE, (gobject.TYPE_GSTRING, gobject.TYPE_GSTRING,)),
        }
    
    archs = {
        'stable':['alpha','amd64','arm','hppa','i386','ia64','mips','mipsel','powerpc','s390','sparc'],
        'testing':['alpha','amd64','arm','armel','hppa','i386','ia64','mips','mipsel','powerpc','s390','sparc'],
        'unstable':['alpha','amd64','arm','armel','hppa','hurd-i386','i386','ia64','m68k','mips','mipsel','powerpc','s390','sparc']}

    def __init__(self, paths, distro, arch):
        gobject.GObject.__init__(self)
        self.current_distro = distro
        self.current_arch = arch
        self.gui = gtk.Builder()
        self.gui.add_from_file(paths.get_in_data_path('debweather.ui'))
        self.dlg_prefs = self.gui.get_object('dlg_prefs')
        self.btn_apply = self.gui.get_object('btn_apply')
        self.cmb_distro = self.gui.get_object('cmb_distro')
        self.cmb_arch = self.gui.get_object('cmb_arch')
        self.lst_distros = self.cmb_distro.get_model()
        self.lst_archs = self.cmb_arch.get_model()
        distro_cell = gtk.CellRendererText()
        arch_cell = gtk.CellRendererText()
        self.cmb_distro.pack_start(distro_cell, True)
        self.cmb_distro.add_attribute(distro_cell, 'text', 0) 
        self.cmb_arch.pack_start(arch_cell, True)
        self.cmb_arch.add_attribute(arch_cell, 'text', 0) 
        self.gui.connect_signals(self)

    def set_current_distro(self, distro):
        self.current_distro = distro
    
    def set_current_arch(self, arch):
        self.current_arch = arch

    def show(self):
        for i,d in enumerate(self.lst_distros):
            if d[0] == self.current_distro:
                self.cmb_distro.set_active(i)

        self.lst_archs.clear()
        for i,arch in enumerate(self.archs[self.current_distro]):
            self.lst_archs.append([arch])
            logging.debug('Appending arch: %s' % arch)
            if arch == self.current_arch:
                self.cmb_arch.set_active(i)
        self.btn_apply.set_sensitive(False)
        self.dlg_prefs.show()

    def on_cmb_distro_changed(self, widget):
        self.lst_archs.clear()
        current_distro = self.lst_distros[self.cmb_distro.get_active()][0]
        for i,arch in enumerate(self.archs[current_distro]):
            self.lst_archs.append([arch])
            logging.debug('Appending arch: %s' % arch)

        self.btn_apply.set_sensitive(False)
        logging.debug("Distro changed")

    def on_cmb_arch_changed(self, widget):
        logging.debug("Arch changed")
        self.btn_apply.set_sensitive(True)

    def on_btn_apply_clicked(self, widget):
        logging.debug("Apply")
        distro = self.cmb_distro.get_active_text()
        arch = self.cmb_arch.get_active_text()
        conf_client = gconf.client_get_default()
        if conf_client.dir_exists('/apps/debian-weather-applet'):
            conf_client.set_string('/apps/debian-weather-applet/distro', distro)
            conf_client.set_string('/apps/debian-weather-applet/arch', arch)
        self.emit('new-preferences', distro, arch)
        self.dlg_prefs.hide()

    def on_btn_cancel_clicked(self, widget):
        logging.debug("Cancel")
        self.dlg_prefs.hide()

gobject.type_register(PreferencesBox)
