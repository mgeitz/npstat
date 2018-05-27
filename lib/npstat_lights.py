#! /usr/bin/env python

"""
Light Queue Consume for NPStat
"""

import time
import random
import Queue
import os

import npstat_settings as settings

try:
  from neopixel import *
except RuntimeError:
  print('Error importing RPi.GPIO! \
         Unfortunately this must be run as root')

LED_FREQ_HZ    = 800000  # LED signal frequency in hertz (usually 800khz)
LED_DMA        = 5       # DMA channel to use for generating signal (try 5)
LED_INVERT     = False   # True to invert the signal (when using NPN transistor level shift)


def initialize(led_count, input_pin, brightness):
  return Adafruit_NeoPixel(led_count, input_pin, LED_FREQ_HZ, LED_DMA, LED_INVERT, brightness)


def colorWipe(light_flag, lights, color, wait_ms=50):
  """Wipe color across display a pixel at a time."""
  for i in range(lights.numPixels()):
    if light_flag.is_set():
      break
    lights.setPixelColor(i, color)
    lights.show()
    time.sleep(wait_ms/1000.0)


def statusWipes(light_queue, event_queue, lights, light_flag):
  """Run wipe of current event"""
  while(not light_flag.is_set()):
    # Run noise if no status
    if light_queue.empty():
      rainbowCycle(lights, light_flag)
    # Run status color
    else:
      status = light_queue.get()
      colorWipe(light_flag, lights, Color(255, 255, 255))   # White wipe
      colorWipe(light_flag, lights,
        Color(status.color[0], status.color[1], status.color[2]))
      colorWipe(light_flag, lights, Color(255, 255, 255))   # White wipe
      light_queue.task_done()
      # Decrement TTL and Resubmit to self
      if status.ttl > 1:
        status.ttl = status.ttl - 1
        light_queue.put(status)
      # Signal Event Removal
      else:
        ttl_event = settings.event('ttl', status.pid, [75, 75, 75], 1)
        event_queue.put(ttl_event)


def turn_off(lights):
  """Turn off all lights (before a clean exit)"""
  for i in range(lights.numPixels()):
    lights.setPixelColor(i, Color(0, 0, 0))
  lights.show()


def wheel(pos):
  """Generate rainbow colors across 0-255 positions."""
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


def rainbow(lights, light_flag, wait_ms=20, iterations=1):
  """Draw rainbow that fades across all pixels at once."""
  for j in range(256 * iterations):
    if light_flag.is_set():
      break
    for i in range(lights.numPixels()):
      lights.setPixelColor(i, wheel((i + j) & 255))
      lights.show()
      time.sleep(wait_ms/1000.0)


def rainbowCycle(lights, light_flag, wait_ms=20, iterations=1):
  """Draw rainbow that uniformly distributes itself across all pixels."""
  for j in range(256 * iterations):
    if light_flag.is_set():
      break
  for i in range(lights.numPixels()):
    lights.setPixelColor(i, wheel(((i * 256 / lights.numPixels()) + j) & 255))
    lights.show()
    time.sleep(wait_ms/1000.0)
