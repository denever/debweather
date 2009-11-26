import logging
import pygtk
pygtk.require('2.0')

import gtk
import gconf

class PreferencesBox:
    distros = ['stable','testing','unstable']
    archs = {
        'stable':['alpha','amd64','arm','hppa','i386','ia64','mips','mipsel','powerpc','s390','sparc'],
        'testing':['alpha','amd64','arm','armel','hppa','i386','ia64','mips','mipsel','powerpc','s390','sparc'],
        'unstable':['alpha','amd64','arm','armel','hppa','hurd-i386','i386','ia64','m68k','mips','mipsel','powerpc','s390','sparc']}
    dialog = None
    cmb_distro = None
    cmb_arch = None

    def __init__(self, paths, current_distro, current_arch):
        self.gui = gtk.Builder()
        self.gui.add_from_file(paths.get_in_data_path('prefbox.glade'))
        self.dialog = self.gui.get_object('prefs')
        self.cmb_distro = self.gui.get_object('cmb_distro')
        self.cmb_arch = self.gui.get_object('cmb_arch')
        self.cmb_distro.set_model(gtk.ListStore(str))
        self.cmb_arch.set_model(gtk.ListStore(str))
        self.gui.connect_signals(self)

        for i,distro in enumerate(self.distros):
            self.cmb_distro.append_text(distro)
            if distro == current_distro:
                self.cmb_distro.set_active(i)

        for i,arch in enumerate(self.archs[current_distro]):
            self.cmb_arch.append_text(arch)
            if arch == current_arch:
                self.cmb_arch.set_active(i)

    def show(self):
        self.dialog.show()

    def on_cmb_distro_changed(self, widget):
        logging.debug("Distro changed")

    def on_cmb_arch_changed(self, widget):
        logging.debug("Arch changed")

    def on_btn_apply_clicked(self, widget):
        logging.debug("Apply")
        distro = self.cmb_distro.get_active_text()
        arch = self.cmb_arch.get_active_text()
        conf_client = gconf.client_get_default()
        if conf_client.dir_exists('/apps/pydebweather'):
            conf_client.set_string('/apps/pydebweather/distro', distro)
            conf_client.set_string('/apps/pydebweather/arch', arch)

        self.dialog.hide()

    def on_btn_cancel_clicked(self, widget):
        logging.debug("Cancel")
        self.dialog.hide()
