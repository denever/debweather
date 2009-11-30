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
import httplib
from xml.etree.ElementTree import XML
from xml.parsers.expat import ExpatError
from preferencesbox import PreferencesBox
from weatherbox import WeatherBox

class WeatherIcon(gtk.Image):
    def __init__(self, paths, size, distro, arch):
        logging.debug("WeatherIcon.__init__")
        gtk.Image.__init__(self)
        self.paths = paths
        self.icon_size = size
        self.distro = distro
        self.arch = arch
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

    def set_unavailable(self, reason):
        self.set_imageicon('pydebweather.png')
        self.set_tooltip_text('Service unavailable %s' % reason)

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
        weather_url = "/edos-debcheck/results/%s/latest/%s/weather.xml" % (self.distro, self.arch)
        logging.debug(weather_url)

        data = str()
        try:
            logging.debug("Connecting to edos.debian.net...")
            conn = httplib.HTTPConnection("edos.debian.net")
            logging.debug("Getting weather_url...")
            conn.request("GET", weather_url)
            logging.debug("Getting response...")
            r1 = conn.getresponse()
            logging.debug(str(r1.getheaders()))
            data = r1.read()
            logging.debug(data)
        except httplib.HTTPException:
            self.set_unavailable('HTTP error')

        try:
            logging.debug('Parsing XML')
            weather_xml = XML(data)
            self.description = weather_xml.getiterator("description")[0].text
            if self.description is None:
                logging.debug("No Description")
            logging.debug("Description: %s" % self.description)
            self.weather = weather_xml.getiterator("index")[0].text
            logging.debug("Weather: %s" % self.weather)
            self.total = weather_xml.getiterator('total')[0].text
            logging.debug("Total: %s" % self.total)
            self.broken = weather_xml.getiterator('broken')[0].text
            logging.debug("Broken: %s" % self.broken)
            self.url = weather_xml.getiterator('url')[0].text
            logging.debug("URL: %s" % self.url)
            self.weather_select[self.weather]()
            logging.debug("End parsing")
        except ExpatError:
            self.set_unavailable('XML Parsing Error')

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
        pb.connect('new-preferences', self.on_new_preferences)
        pb.show()
        logging.debug("Showed preferences")

    def on_new_preferences(self, widget, distro, arch):
        logging.debug("New preferences %s %s" % (distro, arch))
        self.distro = distro
        self.arch = arch
        self.update()

    def show_more(self, obj, label, *data):
        logging.debug("Showing more")
        wb = WeatherBox(self.paths, self.description, self.arch, self.total, self.broken, self.url)
        wb.show()
