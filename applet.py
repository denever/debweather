#!/usr/bin/env python
# -*- Python -*-
###########################################################################
#                        Python Debian Weather                            #
#                        --------------------                             #
#  copyright         (C) 2008  Giuseppe "denever" Martino                 #
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
from xml.etree.ElementTree import XML

logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s %(levelname)-8s %(message)s',
                    datefmt='%a, %d %b %Y %H:%M:%S',
                    filename='/home/denever/applet.log',
                    filemode='w')

class WeatherIcon(gtk.Label):
    description = 'unknown'
    total = 'unknown'
    broken = 'unknown'
    url = 'unknown'
    weather = 0

    def __init__(self, distro, arch):
        self.weather_url = "/edos-debcheck/results/%s/latest/%s/weather.xml" % (distro, arch)

    def set_clear(self):
        self.set_label("Debian Weather: Clear")

    def set_few_clouds(self):
        self.set_label("Debian Weather: Few clouds")

    def set_overcast(self):
        self.set_label("Debian Weather: Overcast")

    def set_shower(self):
        self.set_label("Debian Weather: Shower scattered")

    def set_storm(self):
        self.set_label("Debian Weather: Storm")
        
    def update(self):
        logging.info("Calling weather update")
        logging.info(self.weather_url)

        data = str()
        # try:
        #     logging.info("Connecting to edos.debian.net...")
        #     conn = httplib.HTTPConnection("edos.debian.net")
        #     logging.info("Getting weather_url...")
        #     conn.request("GET", self.weather_url)
        #     logging.info("Getting response...")
        #     r1 = conn.getresponse()
        #     logging.info(str(r1))
        #     data = r1.read()
        #     logging.info(data)
        # except e:
        #     logging.error(str(e))

        # try:
        #     weather_xml = XML(data)
        #     self.description = weather_xml.getiterator("description")[0].text
        #     self.weather = weather_xml.getiterator("index")[0].text            
        #     self.total = weather_xml.getiterator('total')[0].text
        #     self.broken = weather_xml.getiterator('broken')[0].text
        #     self.url = weather_xml.getiterator('url')[0].text
        # except e:
        #     logging.error(str(e))
        self.weather = '1'

        logging.info(self.description)
        logging.info(self.weather)
        logging.info(self.total)
        logging.info(self.broken)
        logging.info(self.url)

        if self.weather == '1':
            self.set_clear()
        if self.weather == '2':
            self.set_few_clouds()
        if self.weather == '3':
            self.set_overcast()
        if self.weather == '4':
            self.set_shower()
        if self.weather == '5':
            self.set_storm()

        return True

def background_show(applet):
    logging.info("background: %s" % applet.get_background())

def sample_factory(applet, iid):
    logging.info("Creating new applet instance")
    weathericon = WeatherIcon('unstable','i386')
    weathericon.set_storm()
    applet.add(weathericon)
    applet.show_all()
    gobject.timeout_add(1000, background_show, applet)
    gobject.timeout_add_seconds(5, weathericon.update)
    return True

print "Starting factory"
gnomeapplet.bonobo_factory("OAFIID:GNOME_PythonAppletSample_Factory",
                           gnomeapplet.Applet.__gtype__,
                           "hello", "0", sample_factory)
print "Factory ended"
