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

    def __init__(self, current_distro, current_arch):
        self.gui = gtk.Builder()
        self.gui.add_from_file(globalconfig.get_in_data_path('prefbox.glade'))
        self.dialog = gui.get_object('prefs')
        self.cmb_distro = gui.get_object('cmb_distro')
        self.cmb_arch = gui.get_object('cmb_arch')
        self.gui.connect_signals(self)

        for i,distro in enumerate(self.distros):
            self.cmb_distro.append_text(distro)
            if distro == current_distro:
                self.cmb_distro.set_active(i)

        for i,arch in enumerate(archs[current_distro]):
            self.cmb_arch.append_text(arch)
            if arch == current_arch:
                self.cmb_archs.set_active(i)

    def show(self):
        self.dialog.show()

    def on_cmb_distro_changed(self):
        logging.debug("Distro changed")

    def on_cmb_arch_changed(self):
        logging.debug("Arch changed")

    def on_btn_apply(self):
        logging.debug("Apply")
        distro = self.distro_combo.get_active_text()
        arch = self.archs_combo.get_active_text()
        conf_client = gconf.client_get_default()
        if conf_client.dir_exists('/apps/pydebweather'):
            conf_client.set_string('/apps/pydebweather/distro', distro)
            conf_client.set_string('/apps/pydebweather/arch', arch)

        self.window.hide()

    def on_btn_cancel(self):
        logging.debug("Cancel")
        self.dialog.hide()
