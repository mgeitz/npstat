#! /usr/bin/env python

import os
import logging
import time
import datetime
from collections import namedtuple

"""
Settings for npstat
"""

def usage():                                                                     
  """Print some helpful things"""                                                
  print NAME + ' -i [input_pin] -b [brightness 1-255] -l [led_count]'     
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
  """Create any missing directories"""
  os.makedirs(ROOT_PATH)
  if not os.path.isdir(LOG_PATH):                                                
    os.makedirs(LOG_PATH)


def init():
  global NAME
  NAME = "npstat"                                                               # Project name
  global event
  event = namedtuple('event', ['type', 'pid', 'color', 'ttl'])                  # Event struct
  global ROOT_PATH
  ROOT_PATH = '/home/duke/.' + NAME + '/'                                       # Path to project directory
  global LOG_PATH
  LOG_PATH = '/var/log/' + NAME + '/'                                           # Path to project log directory
  if not os.path.isdir(ROOT_PATH):
    directories()
  global LOG_FILE
  LOG_FILE = LOG_PATH + NAME + '.log'                                           # Path to project log
  logging.basicConfig(filename = LOG_FILE, level = logging.DEBUG)
