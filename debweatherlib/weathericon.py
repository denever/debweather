import logging

import pygtk
pygtk.require('2.0')

import gtk
import httplib
from xml.etree.ElementTree import XML
from preferencesbox import PreferencesBox

class WeatherIcon(gtk.Image):
    def __init__(self, paths, size, distro, arch):
        logging.debug("WeatherIcon.__init__")
        gtk.Image.__init__(self)
        self.paths = paths
        self.icon_size = size
        self.distro = distro
        self.arch = arch
        self.weather_url = "/edos-debcheck/results/%s/latest/%s/weather.xml" % (distro, arch)
        self.description = 'unknown'
        self.total = 'unknown'
        self.broken = 'unknown'
        self.url = 'unknown'
        self.weather = 0
        self.weather_select = { '1': self.set_clear,
                           '2': self.set_few_clouds,
                           '3': self.set_overcast,
                           '4': self.set_shower,
                           '5': self.set_storm}
    def cleanup(self):
        logging.debug('cleanup')

    def set_unavailable(self):
        self.set_imageicon('pydebweather.png')
        self.set_tooltip_text('Service unavailable')

    def set_clear(self):
        self.set_imageicon('clear.png')
        self.set_tooltip_text("Debian Weather: Clear")

    def set_few_clouds(self):
        self.set_imageicon('few-clouds.png')
        self.set_tooltip_text("Debian Weather: Few clouds")

    def set_overcast(self):
        self.set_imageicon('overcast.png')
        self.set_tooltip_text("Debian Weather: Overcast")

    def set_shower(self):
        self.set_imageicon('shower.png')
        self.set_tooltip_text("Debian Weather: Shower scattered")

    def set_storm(self):
        self.set_imageicon('storm.png')
        self.set_tooltip_text("Debian Weather: Storm")

    def set_icon_size(self, size):
        self.icon_size = size

    def set_imageicon(self, pngname):
        filename = self.paths.get_in_pix_path(pngname)
        temp = gtk.gdk.pixbuf_new_from_file_at_size(filename, self.icon_size, self.icon_size)
        logging.debug("setting image file: %s" % filename)
        self.set_from_pixbuf(temp)

    def update(self):
        logging.debug("Calling weather update")
        logging.debug(self.weather_url)

        data = str()
        try:
            logging.debug("Connecting to edos.debian.net...")
            conn = httplib.HTTPConnection("edos.debian.net")
            logging.debug("Getting weather_url...")
            conn.request("GET", self.weather_url)
            logging.debug("Getting response...")
            r1 = conn.getresponse()
            logging.debug(str(r1))
            data = r1.read()
            logging.debug(data)
        except e:
            logging.error(str(e))
            self.set_unavailable()

        try:
            weather_xml = XML(data)
            self.description = weather_xml.getiterator("description")[0].text
            self.weather = weather_xml.getiterator("index")[0].text
            self.total = weather_xml.getiterator('total')[0].text
            self.broken = weather_xml.getiterator('broken')[0].text
            self.url = weather_xml.getiterator('url')[0].text
        except e:
            logging.error(str(e))
            self.set_unavailable()

        # logging.debug(self.description)
        # logging.debug(self.weather)
        # logging.debug(self.total)
        # logging.debug(self.broken)
        # logging.debug(self.url)
        self.weather_select[self.weather]()

        return True

    def show_about(self, obj, label, *data):
        logging.debug("Show about")
        dlg_about = gtk.AboutDialog()
        dlg_about.set_program_name('pydebweather')
        dlg_about.set_name('Python Debian Weather Applet')
        dlg_about.set_comments('A panel application for monitoring Debian weather conditions')
        dlg_about.set_version('1.0')
        dlg_about.set_copyright('\xC2\xA9 2008-2009 Giuseppe "denever" Martino')
        dlg_about.set_license('This program is licenced under GNU General Public Licence (GPL) version 2.')
        dlg_about.set_authors(['Giuseppe "denever" Martino <martinogiuseppe@gmail.com>'])
        logo = gtk.gdk.pixbuf_new_from_file(self.paths.get_in_pix_path('pydebweather.png'))
        dlg_about.set_logo(logo)
        dlg_about.run()
        dlg_about.destroy()

    def show_prefs(self, obj, label, *data):
        logging.debug("Show preferences")
        pb = PreferencesBox(self.paths, self.distro, self.arch)
        pb.show()
        logging.debug("Showed preferences")
