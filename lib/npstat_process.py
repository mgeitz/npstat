#! /usr/bin/env python

"""
   Program:             NPStat
   File Name:           npstat_process.py

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
   NPStat Event Queue Consumer and Light Queue Producer
"""


import logging
import os

import npstat_settings as settings


def running_pid(pid):
  """Check for inactive pids"""
  try:
    os.kill(pid, 0)
  except OSError:
    return True
  else:
    return False


def prune_pids(active_pids):
  """Remove inactive pids from active pid list"""
  active_pids = [pid for pid in active_pids if not running_pid(pid)]
  return active_pids


def consume_event(event_queue, light_queue, active_pids):
  """Consume and Process new event"""
  if not event_queue.empty():
    new_event = event_queue.get()
    active_pids = prune_pids(active_pids)
    if new_event.pid not in active_pids:
        settings.log('create > event :: ' + new_event.type + ' [' + str(new_event.pid) + '] :: new event')
    if new_event.type == 'ttl' and new_event.pid in active_pids:
      #active_pids.remove(new_event.pid)
      settings.log('event > ignore :: ' + str(new_event.type) + ' [' + str(new_event.pid) + '] :: TTL expire')
    elif new_event.pid not in active_pids:
      settings.log('event > light :: ' + new_event.type + ' [' + str(new_event.pid) + '] :: trigger light event')
      light_queue.put(new_event)
      active_pids.append(new_event.pid)
    event_queue.task_done()
  return active_pids
