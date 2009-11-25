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
import gnomeapplet
import gobject
import httplib
import logging
import sys
import os.path
from xml.etree.ElementTree import XML

logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s %(levelname)-8s %(message)s',
                    datefmt='%a, %d %b %Y %H:%M:%S',
                    filename='/home/denever/applet.log',
                    filemode='w')

class Config:
    def __init__(self, mainfile):
        self.APP_PATH = os.path.dirname(mainfile)
        if self.APP_PATH == '/usr/bin':
            self.PIX_PATH = os.path.join(os.path.dirname(self.APP_PATH), 'share/pixmaps/pydebweather')
            self.DATA_PATH = os.path.join(os.path.dirname(self.APP_PATH), 'share/pydebweather')
        else:
            self.PIX_PATH=os.path.join(self.APP_PATH, 'data/')
            self.DATA_PATH=os.path.join(self.APP_PATH, 'data/')
        logging.debug("self.PIX_PATH: %s" % self.PIX_PATH)
        logging.debug("self.DATA_PATH: %s" % self.DATA_PATH)

    def get_app_path(self):
        return self.APP_PATH
    
    def get_pix_path(self):
        logging.debug("self.PIX_PATH: %s" % self.PIX_PATH)
        return self.PIX_PATH

    def get_in_pix_path(self, file):
        logging.debug("self.PIX_PATH: %s" % self.PIX_PATH)
        return os.path.join(self.PIX_PATH,file)
    
    def get_data_path(self):
        logging.debug("self.DATA_PATH: %s" % self.DATA_PATH)
        return self.DATA_PATH

    def get_in_data_path(self, file):
        logging.debug("self.DATA_PATH: %s" % self.DATA_PATH)
        return os.path.join(self.DATA_PATH,file)

class WeatherIcon(gtk.Image):
    def __init__(self, distro, arch):
        gtk.Image.__init__(self)
        self.config = Config(__file__)
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

    def set_imageicon(self, pngname):
        filename = self.config.get_in_pix_path(pngname)
        temp = gtk.gdk.pixbuf_new_from_file_at_size(filename, 32, 32)
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
        logo = gtk.gdk.pixbuf_new_from_file(self.config.get_in_pix_path('pydebweather.png'))
        dlg_about.set_logo(logo)
        dlg_about.run()
        dlg_about.destroy()

    def show_prefs(self, obj, label, *data):
        logging.debug("Show preferences")

def background_show(applet):
    logging.debug("background: %s" % applet.get_background())

def create_menu(applet, verbs):
    logging.debug("create_menu")
    menu_xml = """
<popup name="button3">
<menuitem name="Item 1" verb="Prefs" _label="_Preferences" pixtype="stock" pixname="gtk-preferences"/>
<separator/>
<menuitem name="Item 2" verb="About" _label="_About" pixtype="stock" pixname="gtk-about"/>
</popup>"""
    applet.setup_menu(menu_xml, verbs, None)

def sample_factory(applet, iid):
    logging.debug("Creating new applet instance")
    wi = WeatherIcon('unstable','i386')
    logging.debug("wi created")
    wi.update()
    logging.debug("wi updated")
    applet.add(wi)
    applet.show_all()
    verbs = [('About', wi.show_about), ('Prefs', wi.show_prefs)]
    create_menu(applet, verbs)
    gobject.timeout_add(1000, background_show, applet)
    gobject.timeout_add_seconds(60, wi.update)
    logging.debug("Returning true")
    return True

print "Starting factory"
gnomeapplet.bonobo_factory("OAFIID:GNOME_DebianWeatherApplet_Factory",
                           gnomeapplet.Applet.__gtype__,
                           "hello", "0", sample_factory)
print "Factory ended"
# pydebweather.png in /usr/share/pixmaps
