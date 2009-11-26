class PreferencesBox:
    dialog = None
    cmb_distro = None
    cmb_arch = None

    def __init__(self):
        self.gui = gtk.Builder()
        self.gui.add_from_file(globalconfig.get_in_data_path('prefbox.glade'))
        self.dialog = gui.get_object('prefs')
        self.cmb_distro = gui.get_object('cmb_distro')
        self.cmb_arch = gui.get_object('cmb_arch')
        self.gui.connect_signals(self)

    def show(self):
        self.dialog.show()

    def on_cmb_distro_changed(self):
        logging.debug("Distro changed")
        
    def on_cmb_arch_changed(self):
        logging.debug("Arch changed")

    def on_btn_apply(self):
        logging.debug("Apply")

    def on_btn_cancel(self):
        logging.debug("Cancel")
