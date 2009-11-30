#!/usr/bin/env python

from distutils.core import setup

setup(name='debweather',
      version='0.1',
      description='Debian Weather Applet',
      author=['Giuseppe Martino'],
      author_email=['denever@users.sf.net'],
      url='http://github.com/denever/debweather',
      scripts=['debweather.py'],
      packages=['debweatherlib']
     )
