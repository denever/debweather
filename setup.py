#!/usr/bin/env python

from distutils.core import setup

setup(name='debian-weather-applet',
      version='1.0',
      description='Debian Weather Applet',
      author=['Giuseppe Martino'],
      author_email=['denever@users.sf.net'],
      url='http://github.com/denever/debian-weather-applet',
      scripts=['debian-weather-applet'],
      packages=['debweatherlib']
     )
