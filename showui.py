#!/usr/bin/python
import pygtk
pygtk.require('2.0')
import gtk
import gconf
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
    conf_client = gconf.client_get_default()    
    distro = str()
    arch = str()
    if not conf_client.dir_exists('/apps/pydebweather'):
       distro = 'unstable'
       arch = 'i386'
    else:
        distro = conf_client.get_string('/apps/pydebweather/distro')
        arch = conf_client.get_string('/apps/pydebweather/arch')

    pb = PreferencesBox(paths, distro, arch)
    pb.show()
    pb.connect('new-preferences', on_new_preferences)
    gtk.main()

if __name__ == "__main__":
    main()
