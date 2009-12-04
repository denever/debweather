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

import os.path
import logging

class Paths:
    def __init__(self, mainfile):
        self.APP_PATH = os.path.dirname(mainfile)
        logging.debug("self.APP_PATH: %s" % self.APP_PATH)        
        if self.APP_PATH == '/usr/bin':
            self.PIX_PATH = os.path.join(os.path.dirname(self.APP_PATH), 'share/pixmaps/debian-weather-applet')
            self.DATA_PATH = os.path.join(os.path.dirname(self.APP_PATH), 'share/debian-weather-applet')
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

    def get_data_path(self):
        logging.debug("self.DATA_PATH: %s" % self.DATA_PATH)
        return self.DATA_PATH

    def get_in_pix_path(self, file):
        logging.debug("self.PIX_PATH: %s" % self.PIX_PATH)
        return os.path.join(self.PIX_PATH,file)

    def get_in_data_path(self, file):
        logging.debug("self.DATA_PATH: %s" % self.DATA_PATH)
        return os.path.join(self.DATA_PATH,file)
