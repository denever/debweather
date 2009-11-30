#!/usr/bin/python
import pygtk
pygtk.require('2.0')
import gtk
import logging
from debweatherlib import Paths
from debweatherlib import PreferencesBox

logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s %(levelname)-8s %(message)s',
                    datefmt='%a, %d %b %Y %H:%M:%S',
                    filename='/home/denever/work/debweather/showui.log',
                    filemode='w')

def on_new_preferences(widget, distro, arch):
    print widget
    print 'New preferences %s %s' % (distro, arch)

def main():
    paths = Paths(__file__)
    pb = PreferencesBox(paths, 'unstable','i386')
    pb.show()
    pb.connect('new-preferences', on_new_preferences)
    gtk.main()

if __name__ == "__main__":
    main()
