#! /usr/bin/env python

"""
NPStat

NCurses Neopixel Status Indicator
"""

import sys
import os
import time
import getopt
import datetime
import logging
import subprocess
import threading
import Queue
import curses

import lib.npstat_settings as settings
import lib.npstat_process as npsprocess
import lib.npstat_lights as npslights
import lib.npstat_curses as npscurses
import lib.npstat_events as npsevents

try:
  from neopixel import Color
except RuntimeError:
  print('Error importing RPi.GPIO! \
         Unfortunately this must be run as root')

__author__ = 'Michael Geitz'
__version__ = '0.0.2'


def initialize():
  """Initialize the application"""
  subprocess.call(['clear'])
  settings.init()
  settings.log('NPStat version ' + __version__)


def np_stat(screen, lights, brightness):
  """Test a small neopixel ring"""
  try:
    # Default light sequence
    light_sequence = npslights.statusWipes

    # Keys which trigger color changes
    light_keys = [curses.KEY_F1, curses.KEY_F2,
                 curses.KEY_F3, curses.KEY_F4,
                 curses.KEY_F5, curses.KEY_F6]

    # Queues
    key_queue = Queue.Queue()
    event_queue = Queue.Queue()
    light_queue = Queue.Queue()

    # Flags
    light_flag = threading.Event()
    event_flag = threading.Event()

    # Threads
    lights.begin()
    light_control = threading.Thread(target=light_sequence,
            args = (light_queue, event_queue, lights, light_flag))
    light_control.daemon = True
    light_control.start()
    read_input = threading.Thread(target=npscurses.read_keys,
            args = (key_queue, screen))
    read_input.daemon = True
    read_input.start()
    event_input = threading.Thread(target=npsevents.scan_events,
            args = (event_queue, event_flag))
    event_input.daemon = True
    event_input.start()

    active_pids = []
    npscurses.redraw_all(screen)
    key = ''
    while key != ord('q') and key != 27:
      # Process Events
      active_pids = npsprocess.consume_event(event_queue, light_queue, active_pids)
      # Process Keys
      if not key_queue.empty():
        key = key_queue.get()
        key_queue.task_done()
      # F2: Set Lights Profile to Status Wipe
      if key == curses.KEY_F2:
        settings.log('Light Profile: Status Wipe')
        light_sequence=npslights.statusWipes
        npscurses.redraw_all(screen)
      # PgUp: Increase Brightness
      elif key == curses.KEY_PPAGE:
        if brightness < 250:
          brightness = brightness + 4
          lights.setBrightness(brightness)
      # PgDn: Decrease Brightness
      elif key == curses.KEY_NPAGE:
        if brightness > 5:
          brightness = brightness - 4
          lights.setBrightness(brightness)
      # F11: Refresh Screen
      elif key == curses.KEY_F11:
        npscurses.redraw_all(screen)
      # F12: Display Help
      elif key == curses.KEY_F12:
        npscurses.help_menu(screen)
        npscurses.redraw_all(screen)
      # Check for Light Profile Change
      if light_control.is_alive() and key in light_keys:
        light_flag.set()
        light_control.join()
        light_flag.clear()
        light_control = threading.Thread(target=light_sequence,
                args = (event_queue, lights, light_flag))
        light_control.daemon = True
        light_control.start()
      time.sleep(0.01)
  except Exception as e:
    settings.log(e)
  if light_control.is_alive():
    light_flag.set()
    light_control.join()
  npslights.turn_off(lights)
  if read_input.is_alive():
    read_input.join()
  if event_input.is_alive():
    event_flag.set()
    event_input.join()


def main(argv):
  """Main method"""

  # Handle Arguements
  input_pin = 0
  brightness = 0
  led_count = 0

  try:
    opts, args = getopt.getopt(sys.argv[1:], 'hi:b:l:',
            ['help', 'input', 'brightness'])
    if not opts:
      settings.usage()
  except getopt.GetoptError:
    settings.usage()
  for opt, arg, in opts:
    if opt in ('-h', '--help'):
      settings.usage()
    elif opt in ('-i', '--input'):
      input_pin = int(arg)
    elif opt in ('-b', '--brightness'):
      brightness = int(arg)
    elif opt in ('-l', '--leds'):
      led_count = int(arg)
    else:
      assert False, "Unhandled Option"

  if not input_pin or not brightness or not led_count:
    settings.usage()

  # Initialize
  initialize()
  screen = npscurses.initialize_screen()
  color_ring = npslights.initialize(led_count, input_pin, brightness)

  # Main show
  np_stat(screen, color_ring, brightness)

  # Cleanup
  settings.log('Exiting')
  npscurses.redraw_all(screen)
  time.sleep(1)
  npscurses.close_screens(screen)


if __name__ == '__main__':
  main(sys.argv[1:])
