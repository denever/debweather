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

    def __init__(self, paths, current_distro, current_arch):
        gobject.GObject.__init__(self)
        self.gui = gtk.Builder()
        self.gui.add_from_file(paths.get_in_data_path('prefbox.ui'))
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

        # self.cmb_distro.set_model(gtk.ListStore(str))
        # self.cmb_arch.set_model(gtk.ListStore(str))
        self.gui.connect_signals(self)

        for i,d in enumerate(self.lst_distros):
            if d[0] == current_distro:
                self.cmb_distro.set_active(i)

        for i,arch in enumerate(self.archs[current_distro]):
            self.lst_archs.append([arch])
            logging.debug('Appending arch: %s' % arch)
            if arch == current_arch:
                self.cmb_arch.set_active(i)
        self.btn_apply.set_sensitive(False)

    def show(self):
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
        if conf_client.dir_exists('/apps/pydebweather'):
            conf_client.set_string('/apps/pydebweather/distro', distro)
            conf_client.set_string('/apps/pydebweather/arch', arch)
        self.emit('new-preferences', distro, arch)
        self.dlg_prefs.hide()

    def on_btn_cancel_clicked(self, widget):
        logging.debug("Cancel")
        self.dlg_prefs.hide()

gobject.type_register(PreferencesBox)
