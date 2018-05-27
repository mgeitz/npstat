#! /usr/bin/env python

import logging
import os

import npstat_settings as settings

"""
Event Queue Consumer and Light Queue Producer for NPStat
"""

def running_pid(pid):
  """Check for inactive pids"""
  try:
    os.kill(pid, 0)
  except OSError:
    return True
  else:
    return False


def prune_pids(new_event, active_pids):
  """Remove inactive pids from active pid list"""
  active_pids = [pid for pid in active_pids if not running_pid(pid)]
  if new_event.type == 'ttl' and new_event.pid in active_pids:
    active_pids.remove(new_event.pid)
  return active_pids


def consume_event(event_queue, light_queue, active_pids):
  """Consume and Process new event"""
  if not event_queue.empty():
    new_event = event_queue.get()
    active_pids = prune_pids(new_event, active_pids)
    if new_event.pid not in active_pids and new_event.pid > 0:
      settings.log('EVENT: ' + new_event.type + ' - PID: ' + str(new_event.pid))
      light_queue.put(new_event)
      active_pids.append(new_event.pid)
    event_queue.task_done()
  return active_pids
