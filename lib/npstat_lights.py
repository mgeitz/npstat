#! /usr/bin/env python

"""
   Program:             NPStat
   File Name:           npstat_lights.py

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
   NPStat Light Queue Consume
"""


import time
import random
import Queue
import os

try:
  from neopixel import *
except RuntimeError:
  print('Error importing RPi.GPIO! \
         Unfortunately this must be run as root')

import npstat_settings as settings


def initialize(led_count, input_pin, brightness):
  """Initialize Neopixels"""
  return Adafruit_NeoPixel(led_count, input_pin,
          settings.config['lights']['led_freq_hz'],
          settings.config['lights']['led_dma'],
          settings.config['lights']['led_invert'],
          brightness)


def status_wipe(light_flag, lights, color, wait_ms=50):
  """Wipe color across pixels"""
  for i in range(lights.numPixels()):
    if light_flag.is_set():
      break
    lights.setPixelColor(i, color)
    lights.show()
    time.sleep(wait_ms/1000.0)


def status_indicator(light_queue, event_queue, lights, light_flag):
  """Run wipe of current event"""
  while(not light_flag.is_set()):
    # Run noise if no status
    try:
      if light_queue.empty():
        status_idle(lights, light_flag, light_queue)
     # Run status color
      else:
        status = light_queue.get()
        settings.log('light > consume :: ' + status.type + ' [' + str(status.pid) + '] :: indicator output (' + str(status.color) + ')')
        status_wipe(light_flag, lights, Color(settings.config['colors']['white'][0],
                                              settings.config['colors']['white'][1],
                                              settings.config['colors']['white'][2]))
        status_wipe(light_flag, lights, Color(status.color[0], status.color[1], status.color[2]))
        status_wipe(light_flag, lights, Color(settings.config['colors']['white'][0],
                                              settings.config['colors']['white'][1],
                                              settings.config['colors']['white'][2]))
        light_queue.task_done()
        # Persist 0 ttl
        if status.ttl <= 0:
          light_queue.put(status)
        # Decrement TTL and Resubmit to self
        elif status.ttl > 1:
          resubmit_event = settings.event(status.type, status.pid, status.color, (status.ttl - 1))
          light_queue.put(resubmit_event)
        # Signal Event Removal
        else:
          settings.log('light > event :: ' + status.type + ' [' + str(status.pid)  + '] :: ttl expire')
          ttl_event = settings.event('ttl', status.pid, settings.config['colors']['yellow'], 1)
          event_queue.put(ttl_event)
    except Exception as e:
      settings.log(e)

def turn_off(lights):
  """Turn off all lights (before a clean exit)"""
  for i in range(lights.numPixels()):
    lights.setPixelColor(i, Color(0, 0, 0))
  lights.show()


def wheel(pos):
  """Generate rainbow colors across 0-255 positions"""
  if pos < 85:
    return Color(pos * 3, 255 - pos * 3, 0)
  elif pos < 170:
    pos -= 85
    return Color(255 - pos * 3, 0, pos * 3)
  else:
    pos -= 170
    return Color(0, pos * 3, 255 - pos * 3)


def breath(lights, light_flag, wait_ms=20, iterations=1):
  """Breath"""
  while(not light_flag.is_set()):
    lights.setPixelColor(255, 255, 255)
    lights.show()
    for i in range(255):
      if light_flag.is_set():
        break
      lights.setBrightness(i)
      i = i + 9
      lights.show()
      time.sleep(wait_ms/1000.0)


def status_idle(lights, light_flag, light_queue, wait_ms=20, iterations=1):
  """Draw rainbow that uniformly distributes itself across all pixels"""
  for each_color in range(256 * iterations):
    if light_flag.is_set() or not light_queue.empty():
      break
    for light in range(lights.numPixels()):
      lights.setPixelColor(light, wheel(((light * 256 / lights.numPixels()) + each_color) & 255))
      lights.show()
      time.sleep(wait_ms/1000.0)
