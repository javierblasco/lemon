#! /usr/bin/env python

# Copyright (c) 2012 Victor Terron. All rights reserved.
# Institute of Astrophysics of Andalusia, IAA-CSIC
#
# This file is part of LEMON.
#
# LEMON is free software: you can redistribute it and/or modify it
# under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.

import ConfigParser
import os.path

CONFIG_FILENAME = '.juicerc'
CONFIG_PATH = os.path.expanduser('~/%s' % CONFIG_FILENAME)

VIEW_SECTION = 'view'
VIEW_SEXAGESIMAL = 'sexagesimal'
VIEW_DECIMAL = 'decimal'
PERIODS_UNIT = 'periods'
PERIODS_DAYS, PERIODS_HHMMSS, PERIODS_SECONDS = range(3)
PLOT_AIRMASSES = 'airmasses'

DEFAULT_VIEW_SEXAGESIMAL = True
DEFAULT_VIEW_DECIMAL = False
DEFAULT_PERIODS_UNIT = PERIODS_HHMMSS
DEFAULT_PLOT_AIRMASSES = True

# The color codes can use any of the following formats supported by matplotlib:
# abbreviations ('g'), full names ('green'), hexadecimal strings ('#008000') or
# a string encoding float on the 0-1 range ('0.75') for gray shades.

COLOR_SECTION = 'colors'
DEFAULT_COLORS = dict(
  U = 'violet',
  B = 'blue',
  V = 'green',
  R = '#ff4246', # light red
  I = '#e81818', # dark red
  Z = 'cyan',
  Y = 'brown',
  J = 'yellow',
  H = 'pink',
  KS = 'orange',
  K = 'orange',
  L = '0.75', # light gray
  M = '0.50' ) # dark gray

class Configuration(ConfigParser.SafeConfigParser):
    """ Just a quite simple wrapper to automatically have the configuration
    file loaded at instantiation and written to disk on deletion"""

    DEFAULT_CONFIG = '\n'.join(
    ["[%s]" % VIEW_SECTION,
     "%s = %d" % (VIEW_SEXAGESIMAL, (1 if DEFAULT_VIEW_SEXAGESIMAL else 0)),
     "%s = %d" % (PERIODS_UNIT, DEFAULT_PERIODS_UNIT),
     "%s = %d" % (VIEW_DECIMAL, (1 if DEFAULT_VIEW_DECIMAL else 0)),
     "%s = %d" % (PLOT_AIRMASSES, (1 if DEFAULT_PLOT_AIRMASSES else 0)),
     '',
     "[%s]" % COLOR_SECTION] +
    ["%s = %s" % (k, v) for k, v in DEFAULT_COLORS.iteritems()])

    def __init__(self, path, update = True):
        """ Parse a configuration file, creating and populating it with
        the default options in case 'path' does not exist """

        ConfigParser.SafeConfigParser.__init__(self)

        if not os.path.exists(path):
            with open(path, 'wt') as fd:
                fd.write(self.DEFAULT_CONFIG)

        self.read([path])
        self.path = path

    def color(self, letter):
        """ Return the color code to be used for a photometric filter """
        return self.get(COLOR_SECTION, letter.upper())

    def __del__(self):
        with open(self.path, 'wt') as fd:
            self.write(fd)
