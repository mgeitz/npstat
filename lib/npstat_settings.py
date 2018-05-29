#! /usr/bin/env python

"""
   Program:             NPStat
   File Name:           npstat_settings.py

   Copyright (C) 2018 Michael Geitz

   This program is free software; you can redistribute it and/or modify
   it under the terms of the GNU General Public License as published by
   the Free Software Foundation; either version 2 of the License, or
   (at your option) any later version.

   This program is distributed in the hope that it will be useful,
   but WITHOUT ANY WARRANTY; without even the implied warranty of
   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
   GNU General Public License for more details.

   You should have received a copy of the GNU General Public License along
   with this program; if not, write to the Free Software Foundation, Inc.,
   51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA.
"""

"""
   NPStat Settings
"""

import sys
import os
import logging
import time
import datetime
import yaml
import pwd
import grp
from collections import namedtuple

"""
Settings for npstat
"""

def usage():
  """Print some helpful things"""
  print 'npstat -i [input_pin] -b [brightness 1-255] -l [led_count]'
  sys.exit(2)


def timestamp():
  """Returns a neat little timestamp for things"""
  unixstamp = int(time.time())
  timestamp = datetime.datetime.fromtimestamp(int(unixstamp))\
      .strftime('%Y-%m-%d_%H:%M:%S')
  return str(timestamp)


def log(message):
  """Effectively just for timestamping all log messages"""
  logging.info('[' + timestamp() + ']: ' + str(message))


def directories():
  """Create default directories"""
  if not os.path.isdir(ROOT_PATH):
    os.makedirs(ROOT_PATH)
  if not os.path.isdir(LOG_PATH):
    os.makedirs(LOG_PATH)


def load_config():
  """Return config file"""
  config_file = open(ROOT_PATH + 'config.yml', 'r+')
  return yaml.load(config_file)


def default_config():
  """Create default config"""
  generated_config= """
# Settings
settings:
  log_path: '/var/log/npstat/'

# Colors - G, R, B
colors:
  light_pink: [159, 250, 181]
  pink: [52, 221, 151]
  red: [0, 209, 0]
  orange: [102, 255, 34]
  yellow: [218, 255, 33]
  green: [221, 51, 0]
  blue: [51, 17, 204]
  indigo: [0, 34, 68]
  violet: [0, 51, 68]
  white: [255, 255, 255]

# Light settings
lights:
  # Neopixel input pin
  input_pin: 18
  # Starting brightness
  brightness: 200
  # Total count of Neopixel LEDs
  count: 12
  # LED signal frequency in hertz (usually 800khz)
  led_freq_hz: 800000
  # DMA channel to use for generating signal (try 5)
  led_dma: 5
  # True to invert the signal (when using NPN transistor level shift)
  led_invert: False
"""

  if not os.path.exists(ROOT_PATH + 'config.yml'):
    with open(ROOT_PATH + 'config.yml', 'w') as new_config:
      yaml.dump(yaml.load(generated_config), new_config, default_flow_style=False)
    new_config.close()
    sudo_user = os.getenv("SUDO_USER")
    if sudo_user is not None:
      uid = pwd.getpwnam(sudo_user).pw_uid
      gid = grp.getgrnam(sudo_user).gr_gid
      os.chown(ROOT_PATH + 'config.yml', uid, gid)


def init():
  """Initialize NPStat Settings"""
  # Set globals
  global ROOT_PATH
  global LOG_PATH
  global LOG_FILE
  global config
  global event
  event = namedtuple('event', ['type', 'pid', 'color', 'ttl'])

  # Confirm user
  if os.getenv("USER") != "root":
    usage()
  elif os.getenv("SUDO_USER") is not None:
    ROOT_PATH = '/home/' + os.getenv("SUDO_USER") + '/.npstat/'
  else:
    ROOT_PATH = '/root/.npstat/'
  LOG_PATH = '/var/log/npstat/'

  # Load config or create defaults
  if not os.path.exists(ROOT_PATH + 'config.yml'):
    directories()
    default_config()

  # Load Config
  config = load_config()

  # Start Log
  LOG_FILE = LOG_PATH + 'npstat.log'
  logging.basicConfig(filename = LOG_FILE, level = logging.DEBUG)
