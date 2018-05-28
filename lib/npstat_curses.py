#! /usr/bin/env python

"""
   Program:             NPStat
   File Name:           npstat_curses.py

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
   NPStat Curses Interface
"""


import curses
import os
import Queue

import npstat_settings as settings


def draw_screen(screen_obj):
  """Draws the main windows using curses"""
  screen_obj.clear()
  screen_obj.box()
  y, x = screen_obj.getmaxyx()
  center_y = y / 2
  center_x = x / 2

  screen_obj.addstr(0, center_x - 6, "|        |",
      curses.color_pair(1))
  screen_obj.addstr(0, center_x - 4, "NPSTAT",
      curses.color_pair(2))

  screen_obj.addstr(1, center_x - x / 2 + 1, "F12 :",
      curses.color_pair(2))
  screen_obj.addstr(1, center_x - x / 2 + 7, "Help Menu",
      curses.color_pair(3))


def draw_textbox(screen_obj):
  """Draws the captured text box"""
  by, bx = screen_obj.getmaxyx()
  offset_y = 5
  offset_x = bx / 12
  textbox = screen_obj.derwin(offset_y + 14, offset_x * 10, offset_y, offset_x)
  textbox.clear()
  textbox.box()

  screen_obj.addstr(offset_y, offset_x * 6 - 5, "|        |",
      curses.color_pair(1))
  screen_obj.addstr(offset_y, offset_x * 6 - 3, "Events",
      curses.color_pair(2))

  with open(settings.LOG_FILE) as t:
    content = t.readlines()
    end = len(content)
    count = 1
    while count < end and count < 18:
      screen_obj.addstr(offset_y - count + 18, offset_x + 1,
         content[end - count][33:].strip(), curses.color_pair(2))
      count = count + 1
    t.close()


def draw_help_menu(screen_obj):
  """Draws help menu."""
  screen_obj.clear()
  screen_obj.box()
  y, x = screen_obj.getmaxyx()
  center_y = y / 2
  center_x = x / 2

  screen_obj.addstr(0, center_x - 8, "|             |",
      curses.color_pair(1))
  screen_obj.addstr(0, center_x - 6, "NPStat Help",
      curses.color_pair(2))

  screen_obj.addstr(1, center_x - x / 2 + 1, "F12 :",
      curses.color_pair(2))
  screen_obj.addstr(1, 5 + center_x - x / 2, "  Console",
      curses.color_pair(3))

  screen_obj.addstr(5, center_x - x / 3, "Key             :",
      curses.color_pair(1))
  screen_obj.addstr(5, center_x - x / 3 + 17, "  Command",
      curses.color_pair(1))

  screen_obj.addstr(7, center_x - x / 3, "F2:             :",
      curses.color_pair(2))
  screen_obj.addstr(7, center_x - x / 3 + 17, "  Status Wipe",
      curses.color_pair(3))

  screen_obj.addstr(8, center_x - x / 3, "F3:             :",
      curses.color_pair(2))
  screen_obj.addstr(8, center_x - x / 3 + 17, "  Toggle Breath",
      curses.color_pair(3))

  screen_obj.addstr(9, center_x - x / 3, "F4:             :",
      curses.color_pair(2))
  screen_obj.addstr(9, center_x - x / 3 + 17, "  Something",
      curses.color_pair(3))

  screen_obj.addstr(10, center_x - x / 3, "PgUp:           :",
      curses.color_pair(2))
  screen_obj.addstr(10, center_x - x / 3 + 17, "  Increase Brightness",
      curses.color_pair(3))

  screen_obj.addstr(11, center_x - x / 3, "pgDn:           :",
      curses.color_pair(2))
  screen_obj.addstr(11, center_x - x / 3 + 17, "  Decrease Brightness",
      curses.color_pair(3))

  screen_obj.addstr(12, center_x - x / 3, "F11:            :",
      curses.color_pair(2))
  screen_obj.addstr(12, center_x - x / 3 + 17, "  Refresh Screen",
      curses.color_pair(3))

  screen_obj.addstr(13, center_x - x / 3, "F12:            :",
      curses.color_pair(2))
  screen_obj.addstr(13, center_x - x / 3 + 17, "  Toggle Help Display",
      curses.color_pair(3))


def draw_toosmall(screen_obj):
  """Draws screen when too small"""
  screen_obj.clear()
  screen_obj.box()
  y, x = screen_obj.getmaxyx()
  center_y = y / 2
  center_x = x / 2

  screen_obj.addstr(center_y, center_x - 10, "Terminal too small.",
      curses.color_pair(1))


def help_menu(screen_obj):
  """Persistant help menu commands."""
  key = ''
  draw_help_menu(screen_obj)
  while key != ord('q') and key != curses.KEY_F12 and key != 27:
    key = screen_obj.getch()
    if key == curses.KEY_RESIZE:
      return


def redraw_all(screen_obj):
  """Redraw entire screen."""
  y, x = screen_obj.getmaxyx()
  if x >= 80 and y >= 30:
    draw_screen(screen_obj)
    draw_textbox(screen_obj)
  else:
    draw_toosmall(screen_obj)


def read_keys(key_queue, screen_obj):
  """Check dem keys"""
  key = ''
  while key != ord('q') and key != 27:
    key = screen_obj.getch()
    key_queue.put(key)


def initialize_screen():
  """Create new screen in terminal"""
  main_screen = curses.initscr()
  os.system('setterm -cursor off')
  curses.start_color()
  curses.use_default_colors()
  curses.noecho()
  curses.cbreak()
  main_screen.keypad(1)
  main_screen.timeout(100)
  curses.init_pair(1, curses.COLOR_WHITE, -1)  # Title
  curses.init_pair(2, curses.COLOR_YELLOW, -1) # Header
  curses.init_pair(3, curses.COLOR_CYAN, -1)   # Subtext
  redraw_all(main_screen)
  return main_screen


def close_screens(screen_obj):
  """Terminate screen_obj"""
  os.system('setterm -cursor on')
  curses.nocbreak()
  screen_obj.keypad(0)
  curses.echo()
  curses.endwin()
