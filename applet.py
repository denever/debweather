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
            self.DATA_PATH = os.path.join(os.path.dirname(self.APP_PATH), 'share/pixmaps/pydebweather')
        else:
            self.DATA_PATH=os.path.join(self.APP_PATH, 'data/')
        logging.info("self.DATA_PATH: %s" % self.DATA_PATH)
            
    def get_app_path(self):
        return self.APP_PATH

    def get_data_path(self):
        return self.DATA_PATH

    def get_in_data_path(self, file):
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

    def set_clear(self):
        logging.info("setting image file: %s" % self.config.get_in_data_path('clear.png'))
        self.set_from_file(self.config.get_in_data_path('clear.png'))
        self.set_tooltip_text("Debian Weather: Clear")

    def set_few_clouds(self):
        self.set_from_file(self.config.get_in_data_path('few-clouds.png'))
        self.set_tooltip_text("Debian Weather: Few clouds")

    def set_overcast(self):
        self.set_from_file(self.config.get_in_data_path('overcast.png'))
        self.set_tooltip_text("Debian Weather: Overcast")

    def set_shower(self):
        self.set_from_file(self.config.get_in_data_path('shower.png'))
        self.set_tooltip_text("Debian Weather: Shower scattered")

    def set_storm(self):
        logging.info(self.config.get_in_data_path('storm.png'))
        self.set_from_file(self.config.get_in_data_path('storm.png'))
        self.set_tooltip_text("Debian Weather: Storm")

    def update(self):
        logging.info("Calling weather update")
        logging.info(self.weather_url)
        self.weather = '1'
        self.weather_select[self.weather]()
        return True

        # data = str()
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
        # self.weather = '1'

        # logging.info(self.description)
        # logging.info(self.weather)
        # logging.info(self.total)
        # logging.info(self.broken)
        # logging.info(self.url)

        # weather_select = { '1': self.set_clear,
        #                    '2': self.set_few_clouds,
        #                    '3': self.set_overcast,
        #                    '4': self.set_shower,
        #                    '5': self.set_storm}

        # weather_select[self.weather]()

def background_show(applet):
    logging.info("background: %s" % applet.get_background())

def sample_factory(applet, iid):
    logging.info("Creating new applet instance")
    wi = WeatherIcon('unstable','i386')
    logging.info("wi created")
    wi.set_storm()
    logging.info("wi stormed")
    applet.add(wi)
    applet.show_all()
    gobject.timeout_add(1000, background_show, applet)
    gobject.timeout_add_seconds(5, wi.update)
    logging.info("Returning true")
    return True

print "Starting factory"
gnomeapplet.bonobo_factory("OAFIID:GNOME_PythonAppletSample_Factory",
                           gnomeapplet.Applet.__gtype__,
                           "hello", "0", sample_factory)
print "Factory ended"
