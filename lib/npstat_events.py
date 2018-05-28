#! /usr/bin/env python

"""
   Program:             NPStat
   File Name:           npstat_events.py

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
   NPStat Events Queue Producer
"""


import subprocess
import time
import re

import npstat_settings as settings


def scan_events(event_queue, event_flag, sleep=10):
  """Scan and queue system events"""
  while(not event_flag.is_set()):
    scan_session(event_queue)
    for i in range(sleep * 2):
      if event_flag.is_set():
        break
      time.sleep(0.5)


def scan_session(event_queue):
  """Scan and queue session events"""
  outer_paren = re.compile("\((.+)\)")
  local_127 = re.compile("^127\.\d{1,3}\.\d{1,3}\.\d{1,3}$")
  local_10 = re.compile("^10\.\d{1,3}\.\d{1,3}\.\d{1,3}$")
  local_192 = re.compile("^192\.168\.\d{1,3}.\d{1,3}$")
  local_172 = re.compile("^172.(1[6-9]|2[0-9]|3[0-1]).[0-9]{1,3}.[0-9]{1,3}$")
  local_tmux = re.compile("^tmux.")
  try:
    whos = subprocess.check_output(['who', '-up'])
    whos = [whos.strip() for whos in whos.splitlines()]
    for who in whos:
      who = re.sub(' +',' ', who)
      who = who.split()
      new_event_ip = who[7][1:-1]
      new_event_pid = who[6]
      if re.match(local_tmux, new_event_ip):
        new_event_type = 'session_tmux'
        new_event_color = settings.config['colors']['green']
        new_event_ttl = 1
      elif re.match(local_127, new_event_ip) is not None or re.match(local_10, new_event_ip) is not None or re.match(local_192, new_event_ip) is not None or re.match(local_172, new_event_ip) is not None:
        new_event_type = 'session_local'
        new_event_color = settings.config['colors']['blue']
        new_event_ttl = 1
      else:
        new_event_type = 'session_remote'
        new_event_color = settings.config['colors']['orange']
        new_event_ttl = 10
      if int(new_event_pid) > 0:
        session_event = settings.event(new_event_type, int(new_event_pid), new_event_color, new_event_ttl)
        event_queue.put(session_event)
  except Exception as e:
    settings.log(e)
