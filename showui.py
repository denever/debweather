#!/usr/bin/python
import pygtk
pygtk.require('2.0')
import gtk
import gconf
import logging
from debweatherlib import Paths
from debweatherlib import WeatherBox

logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s %(levelname)-8s %(message)s',
                    datefmt='%a, %d %b %Y %H:%M:%S',
                    filename='/home/denever/work/debweather/showui.log',
                    filemode='w')

def main():
    paths = Paths(__file__)
    wb = WeatherBox(paths, 'unstable', 'i386', 'puppa', 'puppa', 'puppa')
    wb.show()
    gtk.main()

if __name__ == "__main__":
    main()
